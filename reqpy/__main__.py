#!/usr/bin/python


import click

@click.command()
@click.option("--name", prompt="enter your name", help="fist test")
def hello(name):
    click.echo(f"HELLO {name}")
    
if __name__=="__main__":
    hello()