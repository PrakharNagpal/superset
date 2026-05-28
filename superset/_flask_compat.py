# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Flask 3.x compatibility shim.

Flask 3.0 removed the deprecated ``_app_ctx_stack`` and
``_request_ctx_stack`` objects.  Some third-party extensions pinned to
older releases (e.g. Flask-SQLAlchemy 2.5.x) still reference them at
import time.  This module re-adds thin compatibility wrappers so those
extensions continue to work under Flask 3.x without requiring a full
upgrade of the extension (and its transitive dependency chain).

Import this module **before** any Flask extension that relies on the
removed stacks.
"""

import flask
import flask.globals


class _CompatAppCtxStack:
    """Mimics the old ``LocalStack`` for ``_app_ctx_stack``."""

    @property
    def top(self):  # noqa: ANN201
        try:
            return flask.globals._cv_app.get()
        except LookupError:
            return None


class _CompatRequestCtxStack:
    """Mimics the old ``LocalStack`` for ``_request_ctx_stack``."""

    @property
    def top(self):  # noqa: ANN201
        try:
            return flask.globals._cv_request.get()
        except LookupError:
            return None


if not hasattr(flask, "_app_ctx_stack"):
    flask._app_ctx_stack = _CompatAppCtxStack()

if not hasattr(flask, "_request_ctx_stack"):
    flask._request_ctx_stack = _CompatRequestCtxStack()
