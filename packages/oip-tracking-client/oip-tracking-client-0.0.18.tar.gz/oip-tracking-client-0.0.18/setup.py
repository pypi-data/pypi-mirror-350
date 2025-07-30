from setuptools import setup

setup(
    name="oip-tracking-client",
    version="0.0.18",
    author="Rachid Belmeskine",
    author_email="rachid.belmeskine@gmail.com",
    description="This is the API client of Open Innovation Platform - Tracking",
    long_description=open("README.public.md").read(),
    long_description_content_type="text/markdown",
    # url='https://github.com/...',
    python_requires=">=3.7",
    packages=[
        "oip_tracking_client",
        "oip_tracking_client.enums",
        "oip_tracking_client.monitors",
    ],
    install_requires=[
        "mlflow==2.16.2",
        "deprecated",
        "requests",
        "pandas",
        "typing",
        "numpy",
        "Pillow",
        "matplotlib",
        "plotly",
        "psutil",
    ],
    entry_points={
        "mlflow.request_header_provider": [
            "unused=oip_tracking_client.oip_header_plugin:OipRequestHeaderProvider"
        ]
    },
    extras_require={"amd": ["pyamdgpuinfo"], "nvidia": ["pynvml"]},
    license="PRIVATE LICENSE",
)
