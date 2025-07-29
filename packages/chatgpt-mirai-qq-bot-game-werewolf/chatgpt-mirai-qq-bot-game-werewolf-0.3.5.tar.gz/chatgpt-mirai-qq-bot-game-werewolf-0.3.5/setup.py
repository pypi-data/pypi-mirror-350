from setuptools import setup, find_packages
import io
import os

version = os.environ.get('RELEASE_VERSION', '0.3.5'
'').lstrip('v')

setup(
    name="chatgpt-mirai-qq-bot-game-werewolf",
    version=version,
    packages=find_packages(),
    include_package_data=True,  # 这行很重要
    package_data={
        "game_werewolf": ["example/*.yaml", "example/*.yml"],
    },
    install_requires=[
        "kirara-ai>3.2.0",
        "beautifulsoup4"
    ],
    entry_points={
        'chatgpt_mirai.plugins': [
            'game_werewolf = game_werewolf:GameWerewolfPlugin'
        ]
    },
    author="chuanSir",
    author_email="416448943@qq.com",

    description="GameWerewolfPlugin for lss233/chatgpt-mirai-qq-bot",
    long_description=io.open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chuanSir123/game_werewolf",
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU Affero General Public License v3',
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/chuanSir123/game_werewolf/issues",
        "Documentation": "https://github.com/chuanSir123/game_werewolf/wiki",
        "Source Code": "https://github.com/chuanSir123/game_werewolf",
    },
    python_requires=">=3.8",
)
