import os
from morphocut.core import Pipeline, Call
from morphocut.file import Find, Glob
from morphocut.image import ImageReader
from holocontour.image.safe_image_properties import SafeImageProperties
from morphocut.stream import Progress
from morphocut.str import Format
from morphocut.contrib.ecotaxa import EcotaxaWriter
from morphocut.contrib.zooprocess import CalculateZooProcessFeatures
from holocontour.contour.morpho_custom import HoloContourNode


def pipeline_run(input_folder, output_name, contour_params, lat=None, lon=None, date=None, ext=".png"):
    output_dir = os.path.join(input_folder, "output")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Selected folder: {input_folder}")
    print(f"Files will be extracted to: {output_dir}")

    with Pipeline() as pipeline:
        fn = Find(input_folder, [ext])
        path = Glob(fn)
        basename = Call(lambda x: os.path.splitext(os.path.basename(x))[0], path)

        metadata = {
            "id": Format("{object_id}", object_id=basename),
            "lat": lat,
            "lon": lon,
            "date": date,
        }

        img = ImageReader(path)

        if img.shape == 2:
            img_gray = img[:, :, 0]
        else:
            img_gray = img

        mask, plot = HoloContourNode(img_gray, contour_params=contour_params)

        region_props = SafeImageProperties(mask, img_gray)

        # to handle multiple objects
        # region_props = FindRegions(mask, img_gray, min_area=30)

        object_meta = CalculateZooProcessFeatures(region_props, metadata)

        EcotaxaWriter(
            os.path.join(output_dir, f"EcoTaxa_{output_name}.zip"),
            (basename + ".jpg", img_gray),
            object_meta,
        )

        EcotaxaWriter(
            os.path.join(output_dir, f"EcoTaxa_{output_name}_mask.zip"),
            (basename + ".jpg", mask),
            object_meta,
        )

        if contour_params.get("save_plot"):
            EcotaxaWriter(
                os.path.join(output_dir, f"EcoTaxa_{output_name}_plot.zip"),
                (basename + ".jpg", plot),
                object_meta,
            )

        Progress(fn)

    pipeline.run()
