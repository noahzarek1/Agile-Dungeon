"""Utility functions"""
import os


def get_absolute_path_of_asset(asset_type: str, asset_subtype: str, asset_name: str) -> str:
    """Get the absolute path of the asset file based on its type, subtype, and name

    Args:
        asset_type (str): Type of asset (eg audio, images, other)
        asset_subtype (str): Subtype of asset (eg music/effects, sprites/tiles, fonts/maps)
        asset_name (str): Filename of the asset

    Returns:
        str: Full absolute path of the asset
    """
    directory_name = os.path.dirname(os.path.realpath(__file__))
    relative_path = os.path.join(directory_name, "..", "assets", asset_type, asset_subtype, asset_name)
    return os.path.abspath(relative_path)


def get_absolute_path_of_asset_directory(asset_type: str, asset_subtype: str) -> str:
    """Get the absolute path of the asset directory based on its type and subtype

    Args:
        asset_type (str): Type of asset (eg audio, images, other)
        asset_subtype (str): Subtype of asset (eg music/effects, sprites/tiles, fonts/maps)

    Returns:
        str: Full absolute path of the asset directory
    """
    directory_name = os.path.dirname(os.path.realpath(__file__))
    relative_path = os.path.join(directory_name, "..", "assets", asset_type, asset_subtype)
    return os.path.abspath(relative_path)
