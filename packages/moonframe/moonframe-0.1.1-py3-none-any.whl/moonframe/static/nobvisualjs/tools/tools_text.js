import { view } from "./tools_zoom.js"
import { isTransition } from "./tools_zoom.js"
import { HEIGHT, WIDTH } from "../settings.js"
import { onFocus } from "./tools_zoom.js"

/**
 * [recursive] call circularText only when zoom transition is complete.
 * @param {*} d Selected circle
 * @param {*} node Circle data
 */
export function callTextAfterZoom(d, node) {
    if (isTransition) { // waiting for zoom transition to end
        setTimeout(() => { callTextAfterZoom(d, node) }, 50)
    }
    else {
        // if during the transition another node is selected -> don't call circularText
        // > don't know the focus has changed because it's based on "isTransition" not the transition itself.
        // > there isn't a built in way to check the status of the transition 
        if (d === onFocus) { 
            if (!d.parent) { // root
                node.each(function (d) {
                    circularText(d)
                })
            }
            else {
                if (d.children) {
                    for (const child of d.children) {
                        circularText(child, [WIDTH / 2 - view[0], HEIGHT / 2 - view[1]])
                    }
                }
                circularText(d, [WIDTH / 2 - view[0], HEIGHT / 2 - view[1]])
            }
        }

    }
}

/**
* Draw the name/title of the circle following its circumference.
* @param {*} d Selected circle
* @param {Array} delta (Optional) translation (x,y). Default to [0, 0]
*/
export function circularText(d, delta = [0, 0]) {
    const k = HEIGHT / view[2]
    const r = d.r * k * 1 + 10 * k / (1 + k)

    if (r >= 40) {

        const cx = (d.x - WIDTH / 2 + delta[0]) * k
        const cy = (d.y - HEIGHT / 2 + delta[1]) * k
        const text = d.nameID
        const col = d.colorID
        const svg = d3.select("#main")

        // svg.selectAll(`[id^="circlePath-"]`).remove()
        const path = svg.append("path")
            .attr("id", `circlePath-${d.ID}`)
            .attr("d", `M ${cx + r}, ${cy} A ${r},${r} 0 1,1 ${cx - r}, ${cy} A ${r},${r} 0 1,1 ${cx + r}, ${cy}`)
            .attr("fill", "none")
            .attr("stroke", "none")

        const textElement = svg.append("text")
            .append("textPath")
            .attr("id", `#circleText-${d.ID}`)
            .attr("href", `#circlePath-${d.ID}`)
            .attr("startOffset", "70%")
            .style("text-anchor", "middle")
            // .style("font-size", k.toPrecision(1) == 1 ? `3vh`: d.data.type == "folder" ? `5vh` : `5vh`)
            .style("font-size", `${35 * k / (1 + k)}px`)
            .style("fill", `${col}`)
            .text(text)
            .attr("stroke", "white")
            .attr("stroke-width", 4)
            .attr("letter-spacing", "1.1px")
            .attr("paint-order", "stroke")

        //if the text is too big compared to the circle -> remove    
        // 15% factor is arbitrary (what's look good... ) can be change
        if (textElement.node().parentNode.getComputedTextLength() >= (2 * 3.14 * r) * 0.85) {
            d3.select(textElement.node().parentNode).remove()
        }
    }
}