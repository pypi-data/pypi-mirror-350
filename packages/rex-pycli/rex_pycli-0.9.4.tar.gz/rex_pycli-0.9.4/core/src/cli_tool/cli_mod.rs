use crate::data_handler::{create_time_stamp, get_configuration, ServerState};
use crate::mail_handler::mailer;
use crate::tcp_handler::{save_state, send_to_clickhouse, server_status, start_tcp_server};
use crate::tui_tool::run_tui;
use clap::Parser;
use env_logger::{Builder, Target};
use log::LevelFilter;
use std::env;
use std::fmt::Debug;
use std::io;
use std::path::PathBuf;
use std::process::Stdio;
use std::sync::Arc;
use std::thread;
use std::thread::sleep;
use std::time::Duration;
//use time::format_description::well_known::iso8601::Config;
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::process::Command as TokioCommand;
use tokio::sync::broadcast;
use tokio::sync::Mutex;
use tokio::task;
use tui_logger;
use std::net::TcpListener;
/// A commandline experiment manager
#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    /// desired log level, info displays summary of connected instruments & recent data. debug will include all data, including standard output from Python.
    #[arg(short, long, default_value_t = 2)]
    verbosity: u8,
    /// Email address to receive results
    #[arg(short, long)]
    email: Option<String>,
    /// Time delay in minutes before starting the experiment
    #[arg(short, long, default_value_t = 0)]
    delay: u64,
    /// Number of times to loop the experiment
    #[arg(short, long, default_value_t = 1)]
    loops: u8,
    /// Path to script containing the experimental setup / control flow
    #[arg(short, long)]
    path: PathBuf,
    /// Dry run, will not log data. Can be used for long term monitoring
    #[arg(short = 'n', long, default_value_t = false)]
    dry_run: bool,
    /// Target directory for output path
    #[arg(short, long, default_value_t = get_current_dir())]
    output: String,
    /// Enable interactive TUI mode
    #[arg(short, long)]
    interactive: bool,
    /// Port overide, allows for overiding default port. Will export this as environment variable for devices to utilise.
    #[arg(short = 'P', long)]
    port: Option<String>,
    /// Optional path to config file used by experiment script. Useful when it is critical the script goes unmodified., 
    #[arg(short, long)]
    scirpt_config: Option<String>,
}
/// A commandline experiment viewer
#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct StandaloneArgs {
    // Port the current experiment is running on. If you are running this on the same device it will be 127.0.0.1:7676
    // otherwise, please use the devices IP , device_ip:7676
    #[arg(short, long)]
    address: String,
    /// desired log level, info displays summary of connected instruments & recent data. debug will include all data, including standard output from Python.
    #[arg(short, long, default_value_t = 2)]
    verbosity: u8,
}
// Wrapper for generating python bindings for rex for direct inclusion with other downstream packages.
#[cfg_attr(feature = "extension-module", pyo3::pyfunction)]
pub fn cli_parser_py() {
    let (shutdown_tx, _) = broadcast::channel(1);

    cli_parser_core(shutdown_tx);
}
// Core CLI tool used for both rex adn rex-py
pub fn cli_parser_core(shutdown_tx: broadcast::Sender<()>) {
    let original_args: Vec<String> = std::env::args().collect();

    let mut cleaned_args = process_args(original_args);

    if let Some(first_arg_index) = cleaned_args.iter().position(|arg| !arg.starts_with('-')) {
        cleaned_args[first_arg_index] = "rex".to_string();
    }

    let args = Args::parse_from(cleaned_args);

    let log_level = match args.verbosity {
        0 => LevelFilter::Error,
        1 => LevelFilter::Warn,
        2 => LevelFilter::Info,
        3 => LevelFilter::Debug,
        _ => LevelFilter::Trace,
    };
    if args.interactive {
        let _ = tui_logger::init_logger(log_level);
    } else {
        let mut builder = Builder::new();
        builder
            .filter_level(log_level)
            .target(Target::Stdout)
            .format_timestamp_secs();
        builder.init();
    };
    log::info!(target: "rex", "Experiment starting in {} s", args.delay * 60);
    sleep(Duration::from_secs(&args.delay * 60));
    let interpreter_path_str = match get_configuration() {
        Ok(conf) => match conf.general.interpreter {
            interpreter => interpreter,
        },
        Err(e) => {
            log::error!("failed to get configuration due to: {}", e);
            return;
        }
    };

    let interpreter_path = Arc::new(interpreter_path_str);
    let script_path = Arc::new(args.path);
    let interpreter_path_loop = Arc::clone(&interpreter_path);
    let output_path = Arc::new(args.output);
    if !interpreter_path_loop.is_empty() {
        for _ in 0..args.loops {
            let interpreter_path_clone = Arc::clone(&interpreter_path);
            let script_path_clone = Arc::clone(&script_path);
            log::info!("Server is starting...");
            
            let state = Arc::new(Mutex::new(ServerState::new()));
            
            let shutdown_rx_tcp = shutdown_tx.subscribe();
            let shutdown_rx_server_satus = shutdown_tx.subscribe();
            let shutdown_rx_logger = shutdown_tx.subscribe();
            let shutdown_rx_interpreter = shutdown_tx.subscribe();
            let shutdown_tx_clone_interpreter = shutdown_tx.clone();
            let shutdown_tx_clone_tcp = shutdown_tx.clone();

            let tcp_state = Arc::clone(&state);
            let server_state = Arc::clone(&state);
            let server_state_ch = Arc::clone(&state);
            let port = match get_configuration() {
                Ok(conf) => match conf.general.port {
                    port => port,
                },
                Err(e) => {
                    log::error!("failed to get configuration due to: {}", e);
                    return;
                }
            };
            let port = if is_port_available(&port) {
                port 
            } else {
                log::warn!("Port {} is already in use, checking if a fall back port has been specified", port);
                match args.port {
                    
                    Some(ref fallback_port) => {
                        log::info!("Fall back port found! using it instead and broadcasting the environment variable");
                        fallback_port.clone()
                        },
                        
                    None => {
                        log::error!("No alternative port specified, cancelling run");
                        return}
                }
            };
            match args.scirpt_config {
                Some(ref config) => env::set_var("REX_PROVIDED_CONFIG_PATH", &config),
                None => {}
            };
            env::set_var("REX_PORT", &port);
            
            let tui_thread = if args.interactive {
                Some(thread::spawn(move || {
                    let rt = match tokio::runtime::Runtime::new() {
                        Ok(rt) => rt,
                        Err(e) => {
                            log::error!("Error creating Tokio runtime for TUI: {:?}", e);
                            return;
                        }
                    };
                    let remote = false;
                    match rt.block_on(run_tui("127.0.0.1:7676", remote)) {
                        Ok(_) => log::info!("TUI closed successfully"),
                        Err(e) => log::error!("TUI encountered an error: {}", e),
                    }
                }))
            } else {
                None
            };
            let tcp_server_thread = thread::spawn(move || {

                let addr = format!("127.0.0.1:{port}", port = port);
                let rt = match tokio::runtime::Runtime::new() {
                    Ok(rt) => rt,
                    Err(e) => {
                        log::error!("Error in thread: {:?}", e);
                        return;
                    }
                };
                rt.block_on(start_tcp_server(
                    addr,
                    tcp_state,
                    shutdown_rx_tcp,
                    shutdown_tx_clone_tcp,
                ))
                .unwrap();
            });

            let interpreter_thread = thread::spawn(move || {
                let rt = match tokio::runtime::Runtime::new() {
                    Ok(rt) => rt,
                    Err(e) => {
                        log::error!("Error in thread: {:?}", e);
                        return;
                    }
                };

                if let Err(e) = rt.block_on(start_interpreter_process_async(
                    interpreter_path_clone,
                    script_path_clone,
                    log_level,
                    shutdown_rx_interpreter,
                )) {
                    log::error!("Python process failed: {:?}", e);
                }

                if let Err(e) = shutdown_tx_clone_interpreter.send(()) {
                    log::error!("Failed to send shutdown signal: {:?}", e);
                }
            });

            let printer_thread = thread::spawn(move || {
                let rt = match tokio::runtime::Runtime::new() {
                    Ok(rt) => rt,
                    Err(e) => {
                        log::error!("Error in thread: {:?}", e);
                        return;
                    }
                };

                rt.block_on(server_status(server_state, shutdown_rx_server_satus))
                    .unwrap();
            });
            // Data storage

            let save_state_arc = Arc::clone(&state);
            let file_name_suffix = create_time_stamp(true);

            let output_path_clone = Arc::clone(&output_path);
            let dumper = if !args.dry_run {
                Some(thread::spawn(move || {
                    let rt = match tokio::runtime::Runtime::new() {
                        Ok(rt) => rt,
                        Err(e) => {
                            log::error!("Failed to create Tokio runtime in Dumper Thread: {:?}", e);
                            return None;
                        }
                    };

                    match rt.block_on(save_state(
                        save_state_arc,
                        shutdown_rx_logger,
                        &file_name_suffix,
                        output_path_clone.as_ref(),
                    )) {
                        Ok(filename) => {
                            log::info!("Data storage thread completed successfully.");
                            Some(filename)
                        }
                        Err(e) => {
                            log::error!("Data storage thread encountered an error: {:?}", e);
                            None
                        }
                    }
                }))
            } else {
                let rt = match tokio::runtime::Runtime::new() {
                    Ok(rt) => rt,
                    Err(e) => {
                        log::error!("Failed to create Tokio runtime in Dumper Thread: {:?}", e);
                        return;
                    }
                };

                {
                    let mut state_retention = rt.block_on(state.lock());
                    state_retention.retention = false;
                    log::warn!(
                        "Setting server data retention off - No data will be written to disk"
                    )
                }
                None
            };


            let tcp_server_result = tcp_server_thread.join();
            let interpreter_thread_result = interpreter_thread.join();
            let printer_result = printer_thread.join();
            let dumper_result = match dumper {
                Some(dumper_thread) => match dumper_thread.join() {
                    Ok(resulting) => resulting,
                    Err(e) => {
                        if let Some(err) = e.downcast_ref::<String>() {
                            log::error!("Data Storage thread encountered an error: {}", err);
                        } else if let Some(err) = e.downcast_ref::<&str>() {
                            log::error!("Data Storage thread encountered an error: {}", err);
                        } else {
                            log::error!("Data Storage thread encountered an unknown error.");
                        }
                        None
                    }
                },
                None => None,
            };

            let results = [
                ("TCP Server Thread", tcp_server_result),
                ("Interpreter Process Thread", interpreter_thread_result),
                ("Printer Thread", printer_result),
            ];

            for (name, result) in &results {
                match result {
                    Ok(_) => log::info!("{} shutdown successfully.", name),
                    Err(e) => {
                        if let Some(err) = e.downcast_ref::<String>() {
                            log::error!("{} encountered an error: {}", name, err);
                        } else if let Some(err) = e.downcast_ref::<&str>() {
                            log::error!("{} encountered an error: {}", name, err);
                        } else {
                            log::error!("{} encountered an unknown error.", name);
                        }
                    }
                }
            }
            let output_file = match dumper_result {
                Some(filename) => {
                    log::info!("Data Storage Thread shutdown successfully.");
                    filename
                }
                None => {
                    log::info!(
                        "Data Storage Thread was not running, so no file output has been generated - was this a dry run?"
                    );
                    return;
                }
            };
            let mut clickhouse_thread = None;
            if let Ok(config) = get_configuration() {
                if let Some(clickhouse_config) = config.click_house_server {
                    if !args.dry_run {
                        let handle = thread::spawn(move || {
                            let rt = match tokio::runtime::Runtime::new() {
                                Ok(rt) => rt,
                                Err(e) => {
                                    log::error!("Error in thread: {:?}", e);
                                    return;
                                }
                            };

                            rt.block_on(send_to_clickhouse(server_state_ch, clickhouse_config))
                                .unwrap();
                        });
                        clickhouse_thread = Some(handle);
                    } else {
                    };
                } else {
                    log::warn!("Failed to get Clickhouse config, data will not be logged to clickhouse, however it will be logged locally");
                }
            } else {
                log::error!("Failed to get configuration.");
            };
            match clickhouse_thread {
                Some(tcp_handle) => {
                    let handle = tcp_handle.join();
                    match handle {
                        Ok(_) => log::info!("Clickhouse process shutdown sucessfully"),
                        Err(e) => log::error!("Error in thread {:?}", e),
                    }
                }
                None => {}
            };

            log::info!("The output file directory is: {}", output_path);
            mailer(args.email.as_ref(), &output_file);

            match tui_thread {
                Some(tui_result) => {
                    let result = tui_result.join();
                    match result {
                        Ok(_) => log::info!("Tui hread shutdown successfully."),
                        Err(e) => {
                            if let Some(err) = e.downcast_ref::<String>() {
                                log::error!("Tui thread encountered an error: {}", err);
                            } else if let Some(err) = e.downcast_ref::<&str>() {
                                log::error!("Tui thread encountered an error: {}", err);
                            } else {
                                log::error!("Tui thread encountered an unknown error.");
                            }
                        }
                    }
                }
                None => {}
            };
        }
    } else {
        log::error!("No interpreter path found in the arguments");
    }
}

fn get_current_dir() -> String {
    env::current_dir()
        .unwrap_or_else(|_| PathBuf::from("."))
        .to_str()
        .unwrap()
        .to_string()
}

async fn start_interpreter_process_async(
    interpreter_path: Arc<String>,
    script_path: Arc<PathBuf>,
    log_level: LevelFilter,
    mut shutdown_rx: broadcast::Receiver<()>,
) -> io::Result<()> {
    let level_str = match log_level {
        LevelFilter::Error => "ERROR",
        LevelFilter::Warn => "WARNING",
        LevelFilter::Info => "INFO",
        LevelFilter::Debug => "DEBUG",
        LevelFilter::Trace => "DEBUG",
        LevelFilter::Off => "ERROR",
    };

    let script_extension = script_path
        .as_ref()
        .extension()
        .and_then(|ext| ext.to_str());
    let optional_args = match script_extension {
        Some("py") => vec!["-u"],
        _ => vec![],
    };

    let mut interpreter_process = TokioCommand::new(interpreter_path.as_ref())
        .env("RUST_LOG_LEVEL", level_str)
        .args(&optional_args)
        .arg(script_path.as_ref())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    let stdout = interpreter_process
        .stdout
        .take()
        .expect("Failed to capture stdout");
    let stderr = interpreter_process
        .stderr
        .take()
        .expect("Failed to capture stderr");

    let stdout_reader = BufReader::new(stdout);
    let stderr_reader = BufReader::new(stderr);

    // Spawn async tasks for reading stdout and stderr
    let stdout_task = task::spawn(async move {
        let mut lines = stdout_reader.lines();
        while let Ok(Some(line)) = lines.next_line().await {
            log::debug!(target: "Interpreter", "{}", line);
        }
    });

    let stderr_task = task::spawn(async move {
        let mut in_traceback = false;
        let mut lines = stderr_reader.lines();
        // some python specific error logging (first class support)
        while let Ok(Some(line)) = lines.next_line().await {
            if line.starts_with("Traceback (most recent call last):") {
                in_traceback = true;
                log::error!("{}", line);
            } else if in_traceback {
                log::error!("{}", line);
                if line.trim().is_empty() {
                    in_traceback = false;
                }
            } else if line.contains("(Ctrl+C)") {
                log::warn!("{}", line);
            } else {
                log::debug!("{}", line);
            }
        }
    });
    tokio::select! {
        _ = shutdown_rx.recv() => {
            log::warn!("Received shutdown signal, terminating interpreter process...");
            if let Some(id) = interpreter_process.id() {
                let _ = interpreter_process.kill().await;
                log::info!("Interpreter process (PID: {}) terminated", id);
            }
        }
        status = interpreter_process.wait() => {
            log::info!("Interpreter process exited with status: {:?}", status);
        }
    }
    // Wait for both stdout and stderr tasks to complete
    let _ = tokio::try_join!(stdout_task, stderr_task);

    Ok(())
}

#[cfg_attr(feature = "extension-module", pyo3::pyfunction)]
pub fn cli_standalone() {
    let original_args: Vec<String> = std::env::args().collect();
    //let args = Args::parse_from(original_args);
    let mut cleaned_args = process_args(original_args);

    if let Some(first_arg_index) = cleaned_args.iter().position(|arg| !arg.starts_with('-')) {
        cleaned_args[first_arg_index] = "rex-viewer".to_string();
    }
    let args = StandaloneArgs::parse_from(cleaned_args);

    let log_level = match args.verbosity {
        0 => LevelFilter::Error,
        1 => LevelFilter::Warn,
        2 => LevelFilter::Info,
        3 => LevelFilter::Debug,
        _ => LevelFilter::Trace,
    };

    let _ = tui_logger::init_logger(log_level);

    let tui_thread = Some(thread::spawn(move || {
        let rt = match tokio::runtime::Runtime::new() {
            Ok(rt) => rt,
            Err(e) => {
                log::error!("Error creating Tokio runtime for TUI: {:?}", e);
                return;
            }
        };
        let remote = true;
        match rt.block_on(run_tui(&args.address, remote)) {
            Ok(_) => log::info!("TUI closed successfully"),
            Err(e) => log::error!("TUI encountered an error: {}", e),
        }
    }));

    match tui_thread {
        Some(tui_result) => {
            let result = tui_result.join();
            match result {
                Ok(_) => log::info!("Tui hread shutdown successfully."),
                Err(e) => {
                    if let Some(err) = e.downcast_ref::<String>() {
                        log::error!("Tui thread encountered an error: {}", err);
                    } else if let Some(err) = e.downcast_ref::<&str>() {
                        log::error!("Tui thread encountered an error: {}", err);
                    } else {
                        log::error!("Tui thread encountered an unknown error.");
                    }
                }
            }
        }
        None => {}
    };
}

fn process_args(original_args: Vec<String>) -> Vec<String> {
    //used for removing python inserted args when rex is invoked from a python script
    let cleaned_args = original_args
        .into_iter()
        .filter(|arg| !arg.contains("python"))
        .collect();
    log::warn!("cleaned args: {:?}", cleaned_args);
    cleaned_args
}



fn is_port_available(port: &str) -> bool {
    match TcpListener::bind(format!("127.0.0.1:{}", port)) {
        Ok(_) => true,
        Err(_) => false,
    }
}