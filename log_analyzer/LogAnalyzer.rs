use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::sync::{Arc, Mutex};
use std::thread;
use std::env;

use crossbeam::channel::{unbounded, Receiver}; // message passing between threads
use once_cell::sync::Lazy; // lazily initializing static variables

static LOG_FILE: Lazy<&str> = Lazy::new(|| "C:\\Users\\Caleb\\Documents\\MacroPad\\resources\\MacroPad.log"); // hard coded file location of where the .log file is

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
        None => true, // otherwise dont filter
    };

    let matches_date = match date_filter { // if a date filter exists match it
        Some(d) => line.contains(d), // find anything line that has this date/between date
        None => true, // otherwuse dont filter
    };

    let matches_keyword = match keyword { // if a keyword filter exists match it
        Some(k) => line.to_lowercase().contains(&k.to_lowercase()), // find anything line that has this keyword
        None => true, // otherwise dont filter
    };

    matches_type && matches_date && matches_keyword // must pass all 3 conditions to continue
}

/*
    Functions for each thread which listens to receiver and updates shared counters safely.

    Parameters:
        rx:
            receiver list
        info:
            info type
        warn:
            warn type
        error:
            error type
        total_processed:
            total processed lines after filters (if any)
*/
fn worker(rx: Receiver<String>, info: Arc<Mutex<usize>>, warn: Arc<Mutex<usize>>, error: Arc<Mutex<usize>>, total_processed: Arc<Mutex<usize>>) {
    for line in rx.iter() { // loop over each incoming line
        match classifyLine(&line) { // each line that matches will increment the accourding line
            LogType::Info => *info.lock().unwrap() += 1, // if info then increase info counter
            LogType::Warn => *warn.lock().unwrap() += 1, // if warn then increase warn counter
            LogType::Error => *error.lock().unwrap() += 1, // if error then increase error counter
            LogType::Other => {} // otherwise its something else/unrecognised
        }
        *total_processed.lock().unwrap() += 1; // always (no matter type) increase total
    }
}

/*
    main function (so the programc can actually run).
*/
fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect(); // all command line args to a vector
    let log_type_filter = args.get(1).and_then(|s| match s.to_lowercase().as_str() { // filters by log type
        "info" => Some(LogType::Info), // info sets info
        "warn" => Some(LogType::Warn), // warn sets warn
        "error" => Some(LogType::Error), // error sets error
        _ => None, // otherwise there is no filter
    });
    let date_filter = args.get(2).map(|s| s.as_str()); // date filter
    let keyword_filter = args.get(3).map(|s| s.as_str()); // keyword filter

    let file = File::open(*LOG_FILE)?; // tries to open log file, exit main if fails to do so
    let reader = BufReader::new(file); // wraps file in buffer reader to read file efficiently

    let (tx, rx) = unbounded(); // unbounded channel (tx for sending, rx for receiving)

    let info_count = Arc::new(Mutex::new(0)); // initialize info counter to 0
    let warn_count = Arc::new(Mutex::new(0)); // initialize warn counter to 0
    let error_count = Arc::new(Mutex::new(0)); // initialize error counter to 0
    let total_processed = Arc::new(Mutex::new(0)); // initialize total counter to 0

    let num_threads = 4; // hard code 4 worker threads
    let mut handles = Vec::new(); // vector of threads

    for _ in 0..num_threads { // for each thread
        let rx = rx.clone(); // clone receiver
        let info = Arc::clone(&info_count); // clone info count
        let warn = Arc::clone(&warn_count); // clone warn count
        let error = Arc::clone(&error_count); // clone error count
        let total = Arc::clone(&total_processed); // clone total count

        handles.push(thread::spawn(move || worker(rx, info, warn, error, total))); // make thread run the worker function
    }

    let mut total_lines = 0; // local counter for how many lines sent to worker
    for line in reader.lines() { // loop over every line
        let line = line?; // handle each I/O line with grace
        if filterLine(&line, log_type_filter.clone(), date_filter, keyword_filter) { // apply filters
            println!("{}", line); // print the filtered line to the screen
            tx.send(line).unwrap(); // if passed, send to workers
            total_lines += 1; // increment total lines that have been processed
        }
    }
    drop(tx); // close sending side of worker so they know they are done

    for handle in handles { // wait for all threads to finish
        handle.join().unwrap(); // no error recovery (instant panic if dead)
    }

    println!("\n----------Summary----------\n"); // separates from other output
    println!("Filtered lines read: {}", total_lines); // filtered lines read in
    println!("Filtered log lines processed: {}", *total_processed.lock().unwrap()); // filtered lines processed
    println!("INFO lines: {}", *info_count.lock().unwrap()); // total info processed
    println!("WARN lines: {}", *warn_count.lock().unwrap()); // total warn processed
    println!("ERROR lines: {}", *error_count.lock().unwrap()); // total error processed

    Ok(()) // end main if all was fine
}
