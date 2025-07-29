import click
from geoseeq import (
    Knex,
    SmartTable
)
from geoseeq.id_constructors import (
    project_from_id
)
import pandas as pd


@click.command()
@click.option('-p', '--profile', default=None, help='profile name')
@click.argument("project_id")
def main(profile, project_id):
    knex = Knex.load_profile(profile)
    proj = project_from_id(knex, project_id)
    proj_folder = proj.result_folder("biotiadx::csf::detailed_report").idem()
    dfs = []
    for samp in proj.get_samples():
        result_folder = samp.result_folder("biotiadx::csf::detailed_report")
        if not result_folder.exists():
            continue 
        result_folder = result_folder.get()
        result_file = result_folder.result_file("report.xlsx")
        if not result_file.exists():
            continue
        result_file = result_file.get()
        df = pd.read_excel(result_file.download())
        dfs.append(df)
    df = pd.concat(dfs)
    print(df)
    df["Identified"] = pd.Categorical(df["Identified"], categories=["identified", "not_identified"], ordered=True)
    print(df.dtypes)
    stable = SmartTable(knex, "summary_table")
    stable.create(
        proj_folder,
        without_default_columns=False,
    )
    stable.import_dataframe(df,
         column_types={
             "Sample Name": "sample"
        })


if __name__ == '__main__':
    main()

