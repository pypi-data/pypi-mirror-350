from _typeshed import Incomplete
from tlc.core.builtins.constants.column_names import BOUNDING_BOXES as BOUNDING_BOXES, BOUNDING_BOX_LIST as BOUNDING_BOX_LIST, HEIGHT as HEIGHT, IMAGE as IMAGE, LABEL as LABEL, SAMPLE_WEIGHT as SAMPLE_WEIGHT, SEGMENTATION as SEGMENTATION, WIDTH as WIDTH, X0 as X0, X1 as X1, Y0 as Y0, Y1 as Y1
from tlc.core.objects.table import Table as Table
from tlc.core.objects.tables.from_url.utils import resolve_coco_table_url as resolve_coco_table_url
from tlc.core.url import Url as Url

msg: str
logger: Incomplete

def register_coco_instances(name: str, metadata: dict, json_file: str, image_root: str | None, revision_url: str = '', project_name: str = '', keep_crowd_annotations: bool = True) -> None:
    '''Register a COCO dataset in Detectron2\'s standard format.

    This method works as a drop-in replacement for detectron2.data.datasets.register_coco_instances.

    :References:

    + [COCO data format](https://cocodataset.org/#format-data)
    + [Detectron2 datasets](https://detectron2.readthedocs.io/en/latest/tutorials/datasets.html)

    The original function reads the json file and uses `pycocoapi` to construct a list of dicts
    which are then registered under the key `name` in detectron\'s `DatasetCatalog`.

    These dicts have the following format:

    ```
    {
        "file_name": "COCO_train2014_000000000009.jpg",
        "height": 480,
        "width": 640,
        "image_id": 9,
        "annotations": [
            {
                "bbox": [97.84, 12.43, 424.93, 407.73],
                "bbox_mode": 1,
                "category_id": 16,
                "iscrowd": 0,
                "segmentation": [[...]]
            },
            ...
        ]
    }
    ```

    This function also registers a list of dicts under the key `name` in detectron\'s `DatasetCatalog`, but before the
    data is generated, a TLCTable is resolved. The first time the function is called with a given signature, a 3LC
    table is created. On subsequent calls, the table replaced with the most recent descendant of the
    root table. If the resolved table contains a `weight` column, this value will be sent along in the list of dicts.

    :param name: the name that identifies a dataset, e.g. "coco_2014_train".
    :param metadata: extra metadata associated with this dataset.
    :param json_file: path to the json instance annotation file.
    :param image_root: directory which contains all the images. `None` if the file_name contains a complete path.
    :param revision_url: url to a specific revision of the table. If not provided, the latest revision will be used.
        If the revision is not a descendant of the initial table, an error will be raised.

    :returns: None
    '''
