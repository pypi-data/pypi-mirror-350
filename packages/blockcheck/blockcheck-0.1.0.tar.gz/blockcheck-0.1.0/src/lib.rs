use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;
use reqwest::blocking::Client;
use serde::Deserialize;
use std::thread;
use std::time::Duration;

const BLOCKCHAIN_API_URL: &str = "https://blockchain.info/balance?active={}";
const RATE_LIMIT_DELAY: f64 = 1.0; // Seconds between API calls
const MAX_RETRIES: u32 = 3;

#[derive(Deserialize)]
struct BalanceResponse {
    #[serde(flatten)]
    balances: std::collections::HashMap<String, Wallet>,
}

#[derive(Deserialize)]
struct Wallet {
    final_balance: i64,
    n_tx: i32,
    total_received: i64,
}

#[pyfunction]
fn get_balance(address: String) -> PyResult<(i64, i32, i64)> {
    let client = Client::new();
    let url = BLOCKCHAIN_API_URL.replace("{}", &address);
    let mut retries = 0;

    loop {
        match client.get(&url).send() {
            Ok(response) => {
                if response.status().is_success() {
                    let result: BalanceResponse = response.json().map_err(|e| {
                        PyRuntimeError::new_err(format!("Failed to parse JSON: {}", e))
                    })?;
                    if let Some(wallet) = result.balances.get(&address) {
                        thread::sleep(Duration::from_secs_f64(RATE_LIMIT_DELAY));
                        return Ok((wallet.final_balance, wallet.n_tx, wallet.total_received));
                    } else {
                        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                            "Address not found in response",
                        ));
                    }
                } else {
                    if retries >= MAX_RETRIES {
                        return Err(PyErr::new::<PyRuntimeError, _>(
                            format!("API request failed with status {} after {} retries", response.status(), MAX_RETRIES),
                        ));
                    }
                    retries += 1;
                    thread::sleep(Duration::from_secs(1));
                    continue;
                }
            }
            Err(e) => {
                if retries >= MAX_RETRIES {
                    return Err(PyErr::new::<PyRuntimeError, _>(
                        format!("API request failed after {} retries: {}", MAX_RETRIES, e),
                    ));
                }
                retries += 1;
                thread::sleep(Duration::from_secs(1));
                continue;
            }
        }
    }
}

#[pymodule]
fn blockcheck(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_balance, m)?)?;
    Ok(())
}