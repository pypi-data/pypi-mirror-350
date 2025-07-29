content = r"""
{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "ec2a032c",
   "metadata": {},
   "source": [
    "---\n",
    "date: '{date}'\n",
    "title: '{title}'\n",
    "---"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
"""

content_md = r"""---
date: '{date}'
title: '{title}'
---
"""
content_md_toml = r"""+++
date = '{date}'
title = '{title}'
+++
"""

content_json = r"""
{
    "cell_type": "markdown",
    "id": "ec2a032c",
    "metadata": {},
    "source": [
        "---\n",
        "date: '{date}'\n",
        "title: '{title}'\n",
        "---"
    ]
}"""
