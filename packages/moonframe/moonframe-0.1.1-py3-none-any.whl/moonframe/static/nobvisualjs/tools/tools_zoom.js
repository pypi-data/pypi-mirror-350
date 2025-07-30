import { callTextAfterZoom } from "./tools_text.js"
import { HEIGHT } from "../settings.js"
import { setTooltip } from "./tools_tooltip.js"

export let view
export let onFocus
export let isTransition = false


export function setInitialView(root, node) {
    onFocus = root
    zoomTo([root.x, root.y, root.r * 2], node)
}

/**
 * Main zoom function.
 * To call when you want to zoom on a circle.
 * @param {*} d Selected circle.
 * @param {*} root Packed data.
 * @param {*} node Circle data.
 */
export function zoom(d, root, node) {

    const card = d3.select("#card")
    const tooltip = d3.select("#tooltip")
    const svg = d3.select("#main")
    let zoomfactor = (!d.children) ? 5 : 2

    card.style("opacity", 0)
    tooltip.style("opacity", 0)

    // If zoom append == not click on screen when already at "root"
    if (!(d === onFocus)) {
        svg.selectAll(`textPath`).remove()
        svg.selectAll(`text`).remove()
        svg.selectAll(`[id^="circlePath-"]`).remove()
        onFocus = d
        isTransition = true
    
        const transition = svg.transition()
            .duration(750)
            .tween("zoom", d => {
                const i = d3.interpolateZoom(view, [onFocus.x, onFocus.y, onFocus.r * zoomfactor])
                return t => zoomTo(i(t), node)
            })
    
        transition.on("end", function () { isTransition = false })
        // text
        callTextAfterZoom(d, node)
    }

}

/**
 * Zoom to an element = new view
 * @param {*} v View coordinates.
*/
export function zoomTo(v, node) {
    const k = HEIGHT / v[2]

    view = v

    node.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`)
    node.attr("r", d => d.r * k)

}


/**
 * [recursive] cool effect to locate an element 
 * @param {*} finder Element
 * @param {*} event Event
 */
export function focusOnElement(finder, event, root, node) {

    function ImHere() {
        if (isTransition) { // waiting for zoom transition to end 
            setTimeout(ImHere, 50)
        }
        else {
            const k = HEIGHT / view[2]
            node.each(function (d, i) {
                if (d.nameID == finder.nameID) {
                    d3.select(this).transition().duration(150).attr("r", d.r * k * 1.5)
                        .transition().duration(300).attr("r", d.r * k)
                }
            })
        }
    }

    if (finder.children) {
        // zoom on itself
        if (onFocus !== finder) {
            zoom(finder, root, node)
            event.stopPropagation()
        }
        // setTooltip(finder, event)
    }
    else {
        const finderparent = finder.parent
        // zoom on parent
        if (onFocus !== finderparent) {
            zoom(finderparent, root, node)
            event.stopPropagation()
        }
        setTooltip(finder, event)
        ImHere()
    }

}
