import { zoom, isTransition, onFocus, view } from "./tools_zoom.js"
import { setTooltip } from "./tools_tooltip.js"
import { HEIGHT, WIDTH } from "../settings.js"


/**
 * Creates circles
 * @param {*} root Packed data
 * @returns circles attributes
*/
export function setCircles(root) {
    // set SVG 
    const svg = d3.select("#main")
        .attr("width", WIDTH)
        .attr("height", HEIGHT)
        .attr("viewBox", `-${WIDTH / 2} -${HEIGHT / 2 + 20} ${WIDTH} ${HEIGHT * 1.2}`)
        .attr("style", `max-width: 100%  height: auto display: block  cursor: pointer `)

    // create circles
    const node = svg.append("g") // DOM
        .selectAll("circle")
        .data(root.descendants()) // excluding root
        .join("circle")
        .attr("id", (d, i) => `circle-${i}`)
        .attr("fill", d => d.children ? "white" : d.colorID)
        .attr("stroke", d => d.children ? d.colorID : "black")
        .attr("stroke-width", d => d.children ? 1.5 : 0)
        // interaction
        .on("click", (event, d) => {
            event.preventDefault()
            zoom(d, root, node, HEIGHT)
        })
        .on("mouseover", onMouseEnter)
        .on("mouseout", onMouseLeave)

    return node
}

/**       
 * Mouseon interaction : show tooltip + increase radius (self+all childrens)
 * @param {*} event Mouseon event.
 * @param {*} d Selected circle.
 */
export function onMouseEnter(event, d) {
    const k = HEIGHT / view[2]

    // works only when zoom transition is finished
    if (isTransition === false && onFocus.children && onFocus !== d && d !== onFocus.parent) {
        if (d.children) {
            for (let child of d.descendants()) {
                d3.select(`#circle-${child.ID}`)
                    .transition().duration(100)
                    .attr("r", child.r * k * 1.03)
            }
            d3.select(this)
                .transition().duration(300)
                .attr("r", d.children && d.r * k * 1.05)
        }
        else {
            d3.select(this)
                .transition().duration(300)
                .attr("stroke", "black")
                .attr("stroke-width", 2)

        }
    }
    setTooltip(d, event)
}

/**
 * Mouseout interaction : hide tooltip + radius back to normal  
 * @param {*} event Mouseout event.
 * @param {*} d Selected circle.
 */
export function onMouseLeave(event, d) {
    const tooltip = d3.select("#tooltip")
    const k = HEIGHT / view[2]

    if (d.children) {
        if (isTransition === false) {
            for (let child of d.descendants()) {
                d3.select(`#circle-${child.ID}`)
                    .transition().duration(300)
                    .attr("r", child.r * k)
            }
            d3.select(this)
                .transition().duration(300)
                .attr("r", d.r * k)

        }
    }
    else {
        d3.select(this)
            .transition().duration(300)
            .attr("stroke", null)
            .attr("stroke-width", 0)
    }
    tooltip.style("opacity", 0)

}
