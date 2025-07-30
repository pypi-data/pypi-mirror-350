from ggshu.ggdata import PlotData

class MaudPlotData(PlotData):
    """Specialized plotting functions for Maud output.

    Aliased to ggmaud.


    Parameters
    ----------
    infd: arviz.InferenceData
        Inference data as generated from maud.
    aes: Aesthetics
        created by `aes()`.

    Example
    -------

    ```python
    import pandas as pd
    from ggshu import aes, geom_arrow, ggmaud

    idata = az.from_netcdf("maud_output/idata.nc")

    (ggmaud(df, aes(reaction="reaction", color="flux")) + geom_map()).to_json("shu_data")
    ```
    """
    pass
