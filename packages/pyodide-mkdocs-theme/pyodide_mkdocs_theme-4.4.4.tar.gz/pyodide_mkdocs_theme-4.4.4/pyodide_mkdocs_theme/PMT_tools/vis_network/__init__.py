"""
Python wrapper for vis.js - Network, for Pyodide-MkDocs-Theme by Frédéric Zinelli.

## WARNING:
    Always import `vis_network` as a namespace : wildcard imports or imports using the `from`
    keyword will raise an error.



## Basic usage:

The module provides a python class `NetWork` that will handle most of the logic needed to create
`js.vis.Network` objects, and manage their events subscriptions and lifetime cycles.
These objects should be used to create networks:

```python
import vis_network as vis

network = vis.Network(
    figure_id = 'figure1',
    data = {
        'nodes': [
            { 'id': 1, 'value': 2, 'label': "Algie" },
            { 'id': 2, 'value': 31, 'label': "Alston" },
            { 'id': 3, 'value': 12, 'label': "Barney" },
            { 'id': 4, 'value': 16, 'label': "Coley" },
            { 'id': 5, 'value': 17, 'label': "Grant" },
            { 'id': 6, 'value': 15, 'label': "Langdon" },
            { 'id': 7, 'value': 6, 'label': "Lee" },
            { 'id': 8, 'value': 5, 'label': "Merlin" },
            { 'id': 9, 'value': 30, 'label': "Mick" },
            { 'id': 10, 'value': 18, 'label': "Tod" },
        ],
        'edges': [
            { 'from': 2, 'to': 8, 'value': 3, 'title': "3 emails per week" },
            { 'from': 2, 'to': 9, 'value': 5, 'title': "5 emails per week" },
            { 'from': 2, 'to': 10, 'value': 1, 'title': "1 emails per week" },
            { 'from': 4, 'to': 6, 'value': 8, 'title': "8 emails per week" },
            { 'from': 5, 'to': 7, 'value': 2, 'title': "2 emails per week" },
            { 'from': 4, 'to': 5, 'value': 1, 'title': "1 emails per week" },
            { 'from': 9, 'to': 10, 'value': 2, 'title': "2 emails per week" },
            { 'from': 2, 'to': 3, 'value': 6, 'title': "6 emails per week" },
            { 'from': 3, 'to': 9, 'value': 4, 'title': "4 emails per week" },
            { 'from': 5, 'to': 3, 'value': 1, 'title': "1 emails per week" },
            { 'from': 2, 'to': 7, 'value': 4, 'title': "4 emails per week" },
        ],
    },
    options = {
        'height': '500px',
        'width': '100%',
        'manipulation': True
    }
)
```

All `vis.Network` arguments are optional. If the `figure` argument isn't given, the default id
string from the `{{ figure(...) }}` macro is used.



## Advanced usage:

Aside of the functions/objects defined in the python `vis_network` module, it behaves like
a proxy object toward the equivalent properties of the original JS `vis` object that can be
found in the browser's console once the CDN has been loaded.
Hence, it is always possible to access the original JS tools.

The original JS `vis.Network` class can be accessed through `vis_network.Network.JS_NETWORK`.
It then can be used to build a network entirely using the JS objects, but note that:

1. All the python objects must be converted to JS plain objects using `vis_network.to_js(...)`.
2. You'll have to handle all the data conversions so that the JS Network object can work
   appropriately.
3. You'll lose the automatic handling of hooks and instances lifetime, meaning memory leaks
   could become big, in some situations.

The declaration of hte example above would become:

```python
import vis_network as vis

vis.Network.JS_NETWORK.new(
    vis.target(),   # valeur par défaut de la macro `{{ figure() }}`
    vis.to_js({
        'nodes': vis.DataSet.new(vis.to_js([
            { 'id': 1, 'value': 2, 'label': "Algie" },
            { 'id': 2, 'value': 31, 'label': "Alston" },
            { 'id': 3, 'value': 12, 'label': "Barney" },
            { 'id': 4, 'value': 16, 'label': "Coley" },
            { 'id': 5, 'value': 17, 'label': "Grant" },
            { 'id': 6, 'value': 15, 'label': "Langdon" },
            { 'id': 7, 'value': 6, 'label': "Lee" },
            { 'id': 8, 'value': 5, 'label': "Merlin" },
            { 'id': 9, 'value': 30, 'label': "Mick" },
            { 'id': 10, 'value': 18, 'label': "Tod" },
        ])),
        'edges': vis.DataSet.new(vis.to_js([
            { 'from': 2, 'to': 8, 'value': 3, 'title': "3 emails per week" },
            { 'from': 2, 'to': 9, 'value': 5, 'title': "5 emails per week" },
            { 'from': 2, 'to': 10, 'value': 1, 'title': "1 emails per week" },
            { 'from': 4, 'to': 6, 'value': 8, 'title': "8 emails per week" },
            { 'from': 5, 'to': 7, 'value': 2, 'title': "2 emails per week" },
            { 'from': 4, 'to': 5, 'value': 1, 'title': "1 emails per week" },
            { 'from': 9, 'to': 10, 'value': 2, 'title': "2 emails per week" },
            { 'from': 2, 'to': 3, 'value': 6, 'title': "6 emails per week" },
            { 'from': 3, 'to': 9, 'value': 4, 'title': "4 emails per week" },
            { 'from': 5, 'to': 3, 'value': 1, 'title': "1 emails per week" },
            { 'from': 2, 'to': 7, 'value': 4, 'title': "4 emails per week" },
        ])),
    }),
    vis.to_js({
        'height': '500px',
        'width': '100%',
        'manipulation': True
    })
)
```

Utilities:

* `vis_network.to_js(...)`:

    Utility to convert with the appropriate conversion options the python objects needed to a
    JsProxy that will be usable by the original vis.Network instance in the browser.

* `vis_network.target(figure_id=None)`:

    Utility to extract a HTML container from the DOM with the given id.
    If the argument is None, the default id string from the `{{ figure(...) }}` macro is used.

"""

from collections import defaultdict
from typing import Any, Dict, Tuple, Callable






def __define():

    from functools import wraps
    import js
    from pyodide.ffi import to_js as py_to_js, JsProxy, JsDoubleProxy



    def __getattr__(prop):
        """
        Relay module attributes accesses directly to the js.vis object
        """
        if prop=='__all__':
            raise ImportError(
                "Wildcard imports of p5 is forbidden within Pyodide-MkDocs-Theme context.\n"
                "Import the module as a namespace instead:\n    import p5\n    p5.createCanvas()"
            )
        try:
            return getattr(js.vis, prop)
        except:
            raise AttributeError(f"vis_network.{ prop } is not defined") from None




    def to_js(py_object, *args, **kwargs):
        """
        Automatically convert a python data structure to the equivalent JsProxy (recursively),
        useable with the JS `vis.Network` instances (meaning: it sets the `dict_converter`
        argument to `js.Object.fromEntries` for you).

        NOTE: Try to avoid assigning the created JsProxy objects: this could increase memory
        leak troubles.
        """
        if 'dict_converter' not in kwargs:
            kwargs['dict_converter'] = js.Object.fromEntries

        return py_to_js(py_object, *args, **kwargs)


    def target(figure_id:str=None):
        """
        Extract from the DOM the html tag with the id @figure_id.
        If @figure_id is `None`, the default value for the equivalent argument of the
        `figure(...)` macro is used instead.
        """
        if figure_id is None:
            figure_id = js.config().argsFigureDivId

        container = js.document.getElementById(figure_id)
        if container is None:
            raise ValueError(f"Couldn't find an HTML tag with the {figure_id!r} id.")
        return container





    NEED_DATA_SET: Tuple[str] = 'edges', 'nodes'

    class NetWork:
        """
        PMT class wrapper around a JS vis.Network object.

        Accessed with `vis_network.Network`.
        If you need to work directly with the original JS `vis.Network` class, you can get access
        its JsProxy through `vis_network.Network.JS_NETWORK`. Note that you'll have to convert
        all the data structures appropriately on your own (see module level help).

        Use self.network to access the original JS instance (as a pyodide.ffi.JsProxy).
        For contracts consistency, methods that are defined on the python object must be used,
        instead of calling directly the version on the JsProxy, self.network.
        """

        JS_NETWORK: JsProxy = js.vis.Network    # The original vis.Network class

        network: JsProxy        # JsProxy of the original JS vis.Network instance
        figure_id: str          # Html id of the container holding the graph.


        _INSTANCES: Dict[str,'Network'] = {}
        __proxies: Dict[ str, Dict[int, JsDoubleProxy]]


        def __init__(self, figure_id:str=None, data:dict=None, options:dict=None):
            """
            Create a Network object, which is a wrapper around the original JS vis.Network object.

            @@figure_id: Id of the figure/div in which the Network must be drawn. If `None`,
                        the current default value of the `figure` macro is used.
            @data:       A python dict of nodes and edges (both as lists of dicts). The python
                        instance will handle the conversions to the proper JS data structures
                        for the user.
            @options:    A python dict, with any of the JS available options. Also converted
                        automatically to a proper JS object.
            """
            if figure_id is None:
                figure_id = js.config().argsFigureDivId

            data      = data or {}
            options   = options or {}
            container = target(figure_id)

            if figure_id in self._INSTANCES:
                self._INSTANCES[figure_id].destroy()

            self.figure_id = figure_id
            self._repr     = f"Network({self.figure_id!r}, {data!r}, {options!r})"
            self.__proxies = defaultdict(lambda: defaultdict(dict))
            self.network   = js.vis.Network.new(
                container,
                self._convert(data),
                self._convert(options),
            )


        def __repr__(self): return self._repr


        def _convert(self, obj:dict):
            """
            Convert a dict to a plain JS "root" object, exploring first the dict first layer and
            converting specific values to cis.DataSet objects:
                - nodes value if it is a list
                - edges value if it is a list
            """
            for data_set in NEED_DATA_SET:
                if data_set in obj and isinstance(obj[data_set], list):
                    obj[data_set] = js.vis.DataSet.new(to_js(obj[data_set]))
            return to_js(obj)


        def on(self, event_name:str, cbk:Callable) -> int:
            """
            Create an event handler from a python function for the NetWork, and return the
            id number representing the function handler, so that it is possible to remove
            that specific listener through `self.off(event_name, listener_id)`.

            WARNING: the interface differs from the original vis.Network.on(...) method: if
            you plan on removing manually the event listener later, you'll have to store the
            int value returned by this vis_network.Network.on(...) call so that the Pyodide
            proxy callback can be properly handled.
            """
            proxy = py_to_js(cbk)
            self.__proxies[event_name][proxy.js_id] = proxy
            self.network.on(event_name, proxy)
            return proxy.js_id


        def off(self, event_name:str=None, listener_id:int=None):
            """
            Remove event listeners for the given event, with the given function id.
            Note this method applies only to event handlers that have been created through the
            python `vis_network.Network.on(...)` method.

            @event_name:  If None (then, @listener_id must also be None), remove all the listeners
                        of the Network.
            @listener_id: Id of the listener to remove (as provided as output of `self.on(...)`).
                        If `None`, remove all listeners related to the @event_name.

            @throws: ValueError if arguments are not valid.

            WARNING: This interface differs from the original JS `vis.Network.off` method.
            If you need to remove other listeners, use the underlying JS object's method:
            `vis_network.Network.network.off(...)`
            """
            if None in (event_name, listener_id):
                if event_name is None and listener_id is not None:
                    raise ValueError(
                        "Cannot use vis_network.Network.off python method: when `event_name` is "
                        "`None`, the `listener_id` argument must also be `None`."
                    )
                events = self.__proxies if event_name is None else [event_name]
                for event in events:
                    for proxy_id in self.__proxies[event]:
                        self.off(event, proxy_id)

            else:
                if event_name not in self.__proxies:
                    raise ValueError(f"No {event_name!r} event registered.")

                proxy = self.__proxies[event_name].pop(listener_id, None)
                if proxy is None:
                    raise ValueError(f"No {listener_id!r} listener registered for the {event_name!r} event.")

                self.network.off(event_name, proxy)
                proxy.destroy()
                if not self.__proxies[event_name]:
                    del self.__proxies[event_name]


        def once(self, event_name:str, cbk:Callable):
            """
            Equivalent to the original JS method, handling extra logic related to Pyodide.
            """

            @wraps(cbk)
            def wrapper(*a, **kw):
                out = cbk(*a, **kw)
                self.off(event_name, js_id)
                return out

            js_id = self.on(event_name, wrapper)


        def destroy(self):
            """
            Equivalent to the original JS method, handling extra logic related to Pyodide.
            """
            self.off()
            self.network.destroy()
            self.network = None


    return __getattr__, to_js, target, NetWork




__getattr__, to_js, target, Network = __define()

def __dir__():
    return ['to_js', 'target', 'NetWork']
