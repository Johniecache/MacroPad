use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::sync::{Arc, Mutex};
use std::thread;
use std::env;

use crossbeam::channel::{unbounded, Receiver}; // message passing between threads
use once_cell::sync::Lazy; // lazily initializing static variables

static LOG_FILE: Lazy<&str> = Lazy::new(|| "CHANGE THIS TO YOUR .LOG FILE LOCATION"); // hard coded file location of where the .log file is

#[derive(Clone, PartialEq, Debug)] // automatically generates implementations for Clone, PartialEq and Debug for the enum
enum LogType { // enum to categorize log lines
    Info, // info type
    Warn, // warn type
    Error, // error type
    Other, // other type
}

/*
    Classifies passed line based on the log type.

    Parameters:
        line:
            line of the current log
*/
fn classifyLine(line: &str) -> LogType {
    if line.starts_with("INFO") { // if its of type info
        LogType::Info // set it to LogType info
    } else if line.starts_with("WARN") { // if its of type warn
        LogType::Warn // set it to LogType warn
    } else if line.starts_with("ERROR") { // if its of type error
        LogType::Error // set it to LogType error
    } else { // if its not any of the others
        LogType::Other // set it to LogType other
    }
}

/*
    Filters log lines based on variouys criteria.

    Parameters:
        line:
            line of the current log
        log_type:
            type of log that is passed from the enum
        date_filter:
            lines that contain a specified date
        keyword:
            lines that contain a certain keyword
*/
fn filterLine(line: &str, log_type: Option<LogType>, date_filter: Option<&str>, keyword: Option<&str>) -> bool {
    let matches_type = match log_type { // if type is entered checks what type it is
        Some(t) => classifyLine(line) == t, // send line ot classifyLine method to see if its equal to one in list
        None => true, // set to true
    };

    let matches_date = match date_filter { // 
        Some(d) => line.contains(d),
        None => true,
    };

    let matches_keyword = match keyword {
        Some(k) => line.to_lowercase().contains(&k.to_lowercase()),
        None => true,
    };

    matches_type && matches_date && matches_keyword
}

fn worker(rx: Receiver<String>, info: Arc<Mutex<usize>>, warn: Arc<Mutex<usize>>, error: Arc<Mutex<usize>>, total_processed: Arc<Mutex<usize>>) {
    for line in rx.iter() {
        match classifyLine(&line) {
            LogType::Info => *info.lock().unwrap() += 1,
            LogType::Warn => *warn.lock().unwrap() += 1,
            LogType::Error => *error.lock().unwrap() += 1,
            LogType::Other => {}
        }
        *total_processed.lock().unwrap() += 1;
    }
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let log_type_filter = args.get(1).and_then(|s| match s.to_lowercase().as_str() {
        "info" => Some(LogType::Info),
        "warn" => Some(LogType::Warn),
        "error" => Some(LogType::Error),
        _ => None,
    });
    let date_filter = args.get(2).map(|s| s.as_str());
    let keyword_filter = args.get(3).map(|s| s.as_str());

    let file = File::open(*LOG_FILE)?;
    let reader = BufReader::new(file);

    let (tx, rx) = unbounded();

    let info_count = Arc::new(Mutex::new(0));
    let warn_count = Arc::new(Mutex::new(0));
    let error_count = Arc::new(Mutex::new(0));
    let total_processed = Arc::new(Mutex::new(0));

    let num_threads = 4;
    let mut handles = Vec::new();

    for _ in 0..num_threads {
        let rx = rx.clone();
        let info = Arc::clone(&info_count);
        let warn = Arc::clone(&warn_count);
        let error = Arc::clone(&error_count);
        let total = Arc::clone(&total_processed);

        handles.push(thread::spawn(move || worker(rx, info, warn, error, total)));
    }

    let mut total_lines = 0;
    for line in reader.lines() {
        let line = line?;
        if filterLine(&line, log_type_filter.clone(), date_filter, keyword_filter) {
            tx.send(line).unwrap();
            total_lines += 1;
        }
    }
    drop(tx);

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Filtered lines read: {}", total_lines);
    println!("Filtered log lines processed: {}", *total_processed.lock().unwrap());
    println!("INFO lines: {}", *info_count.lock().unwrap());
    println!("WARN lines: {}", *warn_count.lock().unwrap());
    println!("ERROR lines: {}", *error_count.lock().unwrap());

    Ok(())
}
