import click
import pandas as pd


def carriage_returns(df):
    for index, row in df.iterrows():
        for column, field in row.items():
            try:
                if "\r\n" in field:
                    return index, column, field
            except TypeError:
                continue


def unnamed_columns(df):
    bad_columns = []
    for key in df.keys():
        if "Unnamed" in key:
            bad_columns.append(key)
    return len(bad_columns)


def zero_count_columns(df):
    bad_columns = []
    for key in df.keys():
        if df[key].count() == 0:
            bad_columns.append(key)
    return bad_columns


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--show-data', is_flag=True, help='Display the CSV data')
def main(filename, show_data):
    df = pd.read_csv(filename)
    
    if show_data:
        click.echo(f"\nCSV Data:")
        click.echo(f"length of data: {len(df)}")
        click.echo(f"number of columns: {len(df.columns)}")
        click.echo(df.to_string())
        click.echo("\n")
    
    for column in zero_count_columns(df):
        click.echo(f"Warning: Column '{column}' has no items in it")
    unnamed = unnamed_columns(df)
    if unnamed:
        click.echo(f"Warning: found {unnamed} columns that are Unnamed")
    carriage_field = carriage_returns(df)
    if carriage_field:
        index, column, field = carriage_field
        click.echo((
           f"Warning: found carriage returns at index {index}"
           f" of column '{column}':")
        )
        click.echo(f"         '{field[:50]}'")
