# magma-seismic
Some tools for MAGMA to handle seismic

## Install
```python
pip install magma-seismic
```
## Import module
```python
from magma_seismic.dowload import Download
import magma_seismic
```
## Check version
```python
magma_seismic.__version__
```
## Download from Winston
```python
download = Download(
    station='LEKR',
    channel='EHZ',
    start_date='2025-05-26',
    end_date='2025-05-26',
    overwrite=True,
    verbose=True,
)

download.to_idds(
    use_merge=True, # change to false to disable merging or fill empty data
)
```
### Change winston server (optional)
```python
download.set_client(
    host='winston address',
    port=123456, # winston port
    timeout=30
)
```
## Check download result
```python
download.failed # will show failed download

download.success # will show all successfull download
```