/*
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
*/

/*

ONLY USEFUL FOR MathJax SUBSCRIPTIONS
-------------------------------------


This module is loaded as "text/javascript", for backward compatibility, providing globals to
avoid failure of old codes.

Purposes/notes:

  - hooks files using subscribeWhenReady

  - MathJax replacements through custom_dir override. Note that, in addition to keep backward
    compatibility, loading mathjax-libs.js in a synch way also simplifies A LOT getting everything
    right at load time (because the mathjax cdn is loaded sync...)

  - The functions defined here are available in the global scope, but won't override the ones
    defined in the modules: those are explicitly imported where needed, in the modules.
    On the other hand, jsLogger becomes unusable in non modules...

  - The modules will override these globals with their own once they are loaded.
*/


/**Swallow any kind of call left in a previous version of the theme, in scripts
 * loaded synchronously.
 * */
const jsLogger =()=> null
//*
globalThis.LOGGER_CONFIG = {}
/*/
globalThis.LOGGER_CONFIG = {ACTIVATE:true, all:1}
//*/



/**Drop the current mathJaxUpdate function and hack the window object content to use a new one.
 * */
function subscribeWhenReady(waitId){
    if(waitId !== 'MathJax'){
        throw new Error("Should never use the legacy version of `subscribeWhenReady` for "+waitId)
    }

    // Allow to requeue the update if mathjax is not ready, if the last call was at least 750ms
    // away from now.
    let lastMathJaxUpdateCall = null
    let maxMathJaxAttempts = 50
    const mathJaxTimeDelta = 100           // ms

    function trueMathJaxUpdate(){
        LOGGER_CONFIG.ACTIVATE && console.log('[MathJax] (legacy) - Page formatting')

        if(window.MathJax.startup.output){
            window.MathJax.startup.output.clearCache()
            window.MathJax.typesetClear()
            window.MathJax.texReset()
            window.MathJax.typesetPromise()
            return
        }

        const now = new Date()
        const reschedule = (
            (lastMathJaxUpdateCall===null || now-lastMathJaxUpdateCall > mathJaxTimeDelta)
            && maxMathJaxAttempts-- > 0
        )
        if(reschedule){
            lastMathJaxUpdateCall = now
            setTimeout(trueMathJaxUpdate, mathJaxTimeDelta)

        }else{
            console.error("Cannot update MathJax (CDN failed to load?)")
        }
    }

    if(!window.mathJaxUpdate){
        throw new Error("window.mathJaxUpdate should already be defined...")
    }

    // Hack the function on the fly, so that it always uses the desired behavior, even for users
    // who override the mathjax-libs.js file in PMT:
    window.mathJaxUpdate = trueMathJaxUpdate

    return ()=>0        // SINK!
}