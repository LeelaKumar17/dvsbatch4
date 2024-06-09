import argparse
import json
from Janes.transform import TransformIntara

class Transform:
    def __init__(self, input_json=None, input_context=None, geometry_type="Point"):
        self.input_json = input_json
        self.input_context = input_context
        self.geometry_type = geometry_type

    def transform(self, transformation, mode, output_path=None, file_format=None, longitude=None, latitude=None, flatten=False, separator="|"):
        transformer = TransformIntara(input_json=self.input_json, input_context=self.input_context, geometry_type=self.geometry_type)
        try:
            transformed_data = transformer.transform(
                transformation=transformation,
                mode=mode,
                output_path=output_path,
                file_format=file_format,
                longitude=longitude,
                latitude=latitude,
                flatten=flatten,
                separator=separator
            )
            if mode == "memory":
                return transformed_data
            else:
                print("Transformation complete!")
        except Exception as e:
            print(f"Error: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Transform Intara JSON data into different formats.")
    parser.add_argument("input_json", type=str, help="Path to the input JSON file")
    parser.add_argument("--input_context", type=str, required=false, help="Path to the input context file")
    parser.add_argument("--geometry-type", default="Point", help="Type of geometry (for GeoJSON transformation)")
    parser.add_argument("transformation", type=str, choices=["rdf", "networkx", "edgelist", "geojson"], required=true, help="Type of transformation")
    parser.add_argument("mode", type=str, choices=["file", "memory"], help="Mode of transformation")
    parser.add_argument("--output_path", type=str, help="Output path for the transformed data")
    parser.add_argument("--file_format", type=str, choices=["nt",
"n3",
"ttl",
"trig",
"jsonld",
"networkx",
"graphml",
"csv",
"parquet",
"geojson",
"dataframe",] help="File format for the output data")
    parser.add_argument("--longitude", help="Longitude key (for GeoJSON transformation)")
    parser.add_argument("--latitude", help="Latitude key (for GeoJSON transformation)")
    parser.add_argument("--flatten", action="store_true", help="Flatten JSON data (for GeoJSON transformation)")
    parser.add_argument("--separator", default="|", help="Separator for flattening (for GeoJSON transformation)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    input_json = None
    input_context = None
    # Load input JSON from file
    with open(args.input_json, "r", encoding="utf-8-sig") as f:
        input_json = f.read()
        print("Input JSON Content:", input_json)
        input_json = json.loads(input_json)
    if args.input_context:
        # Load input context from file
        with open(args.input_context, "r", encoding="utf-8-sig") as f:
            input_context = f.read()
            print("Input Context Content:", input_context)
        input_context = json.loads(input_context)

    transformer = Transform(input_json=input_json, input_context=input_context, geometry_type=args.geometry_type)
    transformed_data = transformer.transform(
        transformation=args.transformation,
        mode=args.mode,
        output_path=args.output_path,
        file_format=args.file_format,
        longitude=args.longitude,
        latitude=args.latitude,
        flatten=args.flatten,
        separator=args.separator
    )

    if args.mode == "file":
        if transformed_data:
            with open(args.output_path, "w") as output_file:
                output_file.write(transformed_data)
            print("data written to:",args.output_path)  
        else:
            print("no data was written by transformation")  
    elif args.mode == "memory":
        print("transformed data:") 
        print(transformed_data)           

if __name__ == "__main__":
    main()
