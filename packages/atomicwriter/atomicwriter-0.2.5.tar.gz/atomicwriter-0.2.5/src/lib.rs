use pyo3::exceptions::{PyFileExistsError, PyOSError, PyValueError};
use pyo3::prelude::*;
use std::{fs, io};
use std::{
    io::{BufWriter, Write},
    path::{self, Path, PathBuf},
};

/// Returns the absolute parent directory of a given path,
/// creating it and any necessary ancestors if they don't exist.
fn get_parent_directory(path: impl AsRef<Path>) -> PyResult<PathBuf> {
    let dir = match path.as_ref().parent() {
        Some(parent) if parent == Path::new("") => Path::new("."),
        Some(parent) => parent,
        None => Path::new("."),
    };

    let dir = path::absolute(dir).map_err(|e| PyOSError::new_err(e.to_string()))?;

    // Create the directories if they don't exist.
    fs::create_dir_all(&dir).map_err(|e| PyOSError::new_err(e.to_string()))?;

    Ok(dir)
}

/// A class for writing to a file atomically.
#[pyclass]
struct AtomicWriter {
    #[pyo3(get)]
    destination: PathBuf,
    #[pyo3(get)]
    overwrite: bool,
    // Use Option<T> so that we can take ownership
    // of T in self.commit()
    // Ref: https://github.com/PyO3/pyo3/issues/2225#issuecomment-1073705548
    inner: Option<BufWriter<tempfile::NamedTempFile>>,
}

#[pymethods]
impl AtomicWriter {
    #[new]
    #[pyo3(signature = (destination, *, overwrite=false))]
    fn new(destination: PathBuf, overwrite: bool) -> PyResult<Self> {
        let destination =
            path::absolute(destination).map_err(|e| PyOSError::new_err(e.to_string()))?;
        let dir = get_parent_directory(&destination)?;

        let tmpfile = tempfile::Builder::new()
            .append(true)
            .tempfile_in(dir.as_path())
            .map_err(|e| PyOSError::new_err(e.to_string()))?;

        let writer = BufWriter::new(tmpfile);

        Ok(Self {
            destination,
            overwrite,
            inner: Some(writer),
        })
    }

    #[pyo3(signature = (data, /))]
    fn write_bytes(&mut self, data: &[u8]) -> PyResult<()> {
        self.inner
            .as_mut()
            // ValueError because that's what Python raises.
            //
            // ```python
            // >>> f = open("foo.txt", "w")
            // >>> f.close()
            // >>> f.write("oops")
            // Traceback (most recent call last):
            // File "<python-input-2>", line 1, in <module>
            //     f.write("oops")
            //     ~~~~~~~^^^^^^^^
            // ValueError: I/O operation on closed file.
            // ```
            .ok_or_else(|| PyValueError::new_err("I/O operation on closed file."))?
            .write(data)
            .map_err(|e| PyOSError::new_err(e.to_string()))?;
        Ok(())
    }

    #[pyo3(signature = (data, /))]
    fn write_text(&mut self, data: &str) -> PyResult<()> {
        self.write_bytes(data.as_bytes())
    }

    /// Commit the contents of the temporary file to the destination file.
    fn commit(&mut self) -> PyResult<()> {
        // If we've already committed the file, then
        // self.tempfile will be [`None`] and that
        // means we have to do nothing.
        // TLDR: self.commit() is idempotent.
        if let Some(mut bufwriter) = self.inner.take() {
            // Take ownership of the underlying wrtier.

            // As per docs: "It is critical to call flush before BufWriter<W> is dropped."
            bufwriter
                .flush()
                .map_err(|e| PyOSError::new_err(e.to_string()))?;

            let tmpfile = bufwriter
                .into_inner()
                .map_err(|e| PyOSError::new_err(e.to_string()))?;

            let persist_result = if self.overwrite {
                tmpfile.persist(&self.destination)
            } else {
                tmpfile.persist_noclobber(&self.destination)
            };

            let file = match persist_result {
                Ok(f) => f,
                Err(e) => {
                    if e.error.kind() == io::ErrorKind::AlreadyExists {
                        return Err(PyFileExistsError::new_err(self.destination.clone()));
                    } else {
                        return Err(PyOSError::new_err(e.to_string()));
                    }
                }
            };

            // Clean up if the sync failed.
            if let Err(err) = file.sync_all() {
                match fs::remove_file(&self.destination) {
                    Ok(_) => {}
                    Err(e) => {
                        if e.kind() != io::ErrorKind::NotFound {
                            return Err(PyOSError::new_err(e.to_string()));
                        }
                    }
                }
                return Err(PyOSError::new_err(err.to_string()));
            }
        }
        Ok(())
    }
}

#[pymodule(gil_used = false)]
fn _impl(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<AtomicWriter>()?;
    Ok(())
}
