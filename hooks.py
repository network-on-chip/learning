import os
import shutil

def on_post_build(config):
    """
    Ensure static assets (including book.pdf and vendor libraries)
    are mirrored into localized subdirectories (such as site/zh/assets)
    so relative and root-relative asset URLs resolve seamlessly without 404s.
    """
    site_dir = config['site_dir']
    src_assets = os.path.join(site_dir, 'assets')
    zh_dir = os.path.join(site_dir, 'zh')
    zh_assets = os.path.join(zh_dir, 'assets')

    if os.path.exists(zh_dir) and os.path.exists(src_assets):
        if not os.path.exists(zh_assets):
            try:
                # Attempt symlink first for efficiency
                os.symlink(os.path.relpath(src_assets, zh_dir), zh_assets)
            except (OSError, AttributeError):
                shutil.copytree(src_assets, zh_assets)
