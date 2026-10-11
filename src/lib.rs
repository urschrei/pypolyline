//! Python bindings for the [`polyline`](https://crates.io/crates/polyline) crate.
//!
//! Coordinates are `(x, y)`, i.e. `(longitude, latitude)`, which is the opposite of the order
//! used in the Polyline algorithm's first-party documentation.

use geo_types::Coord;
use pyo3::buffer::PyBuffer;
use pyo3::exceptions::{PyRuntimeError, PyTypeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyString};

const DECODE_ERROR: &str = "Polyline could not be decoded. Is it valid?";

/// Only Google (5) and OSRM / Valhalla (6) precisions are supported
fn check_precision(precision: i64) -> PyResult<u32> {
    match precision {
        5 | 6 => Ok(precision as u32),
        _ => Err(PyValueError::new_err(format!(
            "precision must be 5 or 6, got {precision}"
        ))),
    }
}

/// Copy `coords` into a `Vec` of coordinates.
///
/// Any object exposing a float64 buffer (e.g. a NumPy array, contiguous or not) is read directly,
/// and must have shape `(N, 2)`. Anything else must be a sequence of `(x, y)` pairs.
fn extract_coords(coords: &Bound<'_, PyAny>) -> PyResult<Vec<Coord<f64>>> {
    if let Ok(buf) = PyBuffer::<f64>::get(coords) {
        match buf.shape() {
            [_, 2] | [0] => {}
            shape => {
                return Err(PyValueError::new_err(format!(
                    "coordinates must have shape (N, 2), got {shape:?}"
                )));
            }
        }
        // Read C-contiguous buffers in place, and copy anything else into C order first
        let py = coords.py();
        return Ok(match buf.as_slice(py) {
            Some(cells) => cells
                .chunks_exact(2)
                .map(|c| Coord {
                    x: c[0].get(),
                    y: c[1].get(),
                })
                .collect(),
            None => buf
                .to_vec(py)?
                .chunks_exact(2)
                .map(|c| Coord { x: c[0], y: c[1] })
                .collect(),
        });
    }
    let pairs: Vec<[f64; 2]> = coords.extract().map_err(|e| {
        let err = PyValueError::new_err("coordinates must be a sequence of (x, y) number pairs");
        err.set_cause(coords.py(), Some(e));
        err
    })?;
    Ok(pairs.into_iter().map(|[x, y]| Coord { x, y }).collect())
}

/// Encode coordinates as a Polyline.
///
/// Input: an (N, 2) array-like of lon, lat coordinates, and a precision int (5 for Google, 6 for OSRM / Valhalla).
/// Output: an encoded Polyline as bytes.
///
/// Raises ValueError for a bad precision or coordinate shape, and RuntimeError if the coordinates
/// cannot be encoded.
///
/// Example: encode_coordinates([[-120.2, 38.5], [-120.95, 40.7], [-126.453, 43.252]], 5)
/// Result: b"_p~iF~ps|U_ulLnnqC_mqNvxq`@"
#[pyfunction]
fn encode_coordinates<'py>(
    py: Python<'py>,
    coords: &Bound<'py, PyAny>,
    precision: i64,
) -> PyResult<Bound<'py, PyBytes>> {
    let precision = check_precision(precision)?;
    let coords = extract_coords(coords)?;
    let encoded = py
        .detach(|| polyline::encode_coordinates(coords, precision))
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
    Ok(PyBytes::new(py, encoded.as_bytes()))
}

/// Decode an encoded Polyline to coordinates.
///
/// Input: a Polyline (bytes or str), and a precision int (5 for Google, 6 for OSRM / Valhalla).
/// Output: a list of lon, lat coordinates.
///
/// Raises ValueError for a bad precision, and RuntimeError if the Polyline cannot be decoded.
///
/// Example: decode_polyline(b"_p~iF~ps|U_ulLnnqC_mqNvxq`@", 5)
/// Result: [[-120.2, 38.5], [-120.95, 40.7], [-126.453, 43.252]]
#[pyfunction]
fn decode_polyline(
    py: Python<'_>,
    polyline: &Bound<'_, PyAny>,
    precision: i64,
) -> PyResult<Vec<[f64; 2]>> {
    let precision = check_precision(precision)?;
    let text = if let Ok(b) = polyline.cast::<PyBytes>() {
        std::str::from_utf8(b.as_bytes()).ok()
    } else if let Ok(s) = polyline.cast::<PyString>() {
        s.to_str().ok()
    } else {
        return Err(PyTypeError::new_err(format!(
            "polyline must be bytes or str, not {}",
            polyline.get_type().name()?
        )));
    }
    .ok_or_else(|| PyRuntimeError::new_err(DECODE_ERROR))?;
    let decoded = py
        .detach(|| polyline::decode_polyline(text, precision))
        .map_err(|_| PyRuntimeError::new_err(DECODE_ERROR))?;
    Ok(decoded.into_iter().map(|c| [c.x, c.y]).collect())
}

#[pymodule(gil_used = false)]
mod cutil {
    #[pymodule_export]
    use super::{decode_polyline, encode_coordinates};
}
