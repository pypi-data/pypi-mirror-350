from pyehr import extract


def test_stata():
    return extract.extract_from_stata(
        table_dir="/mnt/iusers01/ja01/p28917yz/developments/data/aurum_sample/stata",
        file_ext="dta",
        id_col="patid",
        values=[6921475120038, 2924482520038, 6397925820599, 6400844220599],
        cores=8,
        output_dir="/mnt/iusers01/ja01/p28917yz/developments/data/pycprd_test_output",
        single_file=True,
    )


def test_txt():
    return extract.extract_from_table(
        table_dir="/mnt/iusers01/ja01/p28917yz/developments/data/aurum_sample/txt",
        file_ext="txt",
        id_col="patid",
        values=[6921475120038, 2924482520038, 6397925820599, 6400844220599],
        output_dir="/mnt/iusers01/ja01/p28917yz/developments/data/pycprd_test_output",
        single_file=True,
        output_name="output_test",
        output_ext="csv",
    )


if __name__ == "__main__":
    test_txt()
