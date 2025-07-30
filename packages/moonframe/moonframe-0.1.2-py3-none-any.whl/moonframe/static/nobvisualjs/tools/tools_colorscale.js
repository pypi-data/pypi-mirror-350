import { colorLegend } from "./tools_colorLegend.js"

const listColor = [
    d3.interpolatePlasma,
    d3.interpolateTurbo,
    d3.interpolateViridis,
    d3.interpolateInferno,
    d3.interpolateMagma,
    d3.interpolateCividis,
    d3.interpolateWarm,
    d3.interpolateCool,
    d3.interpolateBlues,
    d3.interpolateGreens,
    d3.interpolateGreys,
    d3.interpolateOranges,
    d3.interpolatePurples,
    d3.interpolateReds,
    d3.interpolateBuGn,
    d3.interpolateBuPu,
    d3.interpolateGnBu,
    d3.interpolateOrRd,
    d3.interpolatePuBuGn,
    d3.interpolatePuBu,
    d3.interpolatePuRd,
    d3.interpolateRdPu,
    d3.interpolateYlGnBu,
    d3.interpolateYlGn,
    d3.interpolateYlOrBr,
]

let colID = 0
let customScale = {}

/**
 * Create the color scale according to the colorby metric. 
 * The scale is then stored in "color" that can be used as
 * "color(d.data[colorBy])"" to get the corresponding color.
 * @param {*} root Packed data
 * @param {*} colorKey Key in the data of the color
 * @param {*} legend Custom color scale
 * @returns Color scale
 */
export function createColorScale(root, colorKey, legend) {
    const legendSvg = d3.select("#legend")
    let color
    if (legend) { // custom scale
        color = d3.scaleOrdinal()
            .domain(Object.values(legend))
            .range(Object.keys(legend))

        const lg = legendSvg.append("g")
        lg.call(d3.legendColor().scale(color))

        d3.select("#scaleSelector").append("option").html("custom scale")
    }
    else {
        if (typeof root.descendants()[0].data[colorKey] == "string") { // category 
            color = d3.scaleOrdinal()
                .domain([...new Set(root.descendants().map(d => d.data[colorKey]))])
                .range(d3.schemeObservable10)

            const lg = legendSvg.append("g")
            lg.call(d3.legendColor().scale(color))
            const current_height = lg.node().getBBox().height + 10
            legendSvg.attr("height", current_height)
                .attr("width", 18)
                .attr("viewBox", [0, 0, 18, current_height])
                .style("overflow", "visible")
                .style("display", "block")

        }
        else { // continuous
            color = d3.scaleSequential(
                [d3.min(root.descendants(), d => d.data[colorKey]), d3.max(root.descendants(), d => d.data[colorKey])]
                , listColor[colID])
            colorLegend({ color: color })
        }
        d3.select("#scaleSelector").append("option").html(colorKey).attr("value", colorKey)
    }
    return color
}

/**
 * When an event occurs, change the color scale.
 * @param {*} root Packed data.
 * @param {string} colorKey Key in the data for the color.
 * @param {boolean} isLog Log scale (True) or linear (False).
 * @returns 
 */
export function changeColorScale(root, colorKey, isLog) {
    const legendSvg = d3.select("#legend")
    let color
    legendSvg.selectAll("*").remove()

    if (typeof root.descendants()[0].data[colorKey] == "string") { // category 
        if (Object.keys(customScale).includes(colorKey)) { // in memory
            color = customScale[colorKey]
        }
        else {
            color = d3.scaleOrdinal()
                .domain([...new Set(root.descendants().map(d => d.data[colorKey]))])
                .range(d3.schemeObservable10)
        }

        const lg = legendSvg.append("g")
        lg.call(d3.legendColor().scale(color))
        const current_height = lg.node().getBBox().height + 10
        legendSvg.attr("height", current_height)
            .attr("viewBox", [0, 0, 18, current_height])
    }
    else { // continuous
        if (isLog) { // log
            color = d3.scaleSequentialLog(
                [1, d3.max(root.descendants(), d => d.data[colorKey])]
                , listColor[colID])
        } else { // linear
            color = d3.scaleSequential(
                [d3.min(root.descendants(), d => d.data[colorKey]), d3.max(root.descendants(), d => d.data[colorKey])]
                , listColor[colID])
        }
        colorLegend({ color: color })
        d3.transition().duration(200).select("#block_under_legend").style("margin-top", "0")
    }
    return color
}

/**
 * Change single color in d3.scaleOrdinal
 * @param {Object} color Color scale
 * @param {int} index Index of the color
 * @param {string} newColor New color
 * @returns 
 */
export function changeSingleColInOrdinal(color, index, newColor) {
    let range = color.range()
    range[index] = newColor
    color.range(range)
}

/**
 * Add +1 to colID
 */
export function increaseColID() {
    colID === listColor.length - 1 ? colID = 0 : colID += 1
}

/**
 * Add a custom color scale in custom scale.
 * @param {string} key Color key
 * @param {object} value Color scale
 */
export function addCustomColor(key, value) {
    customScale[key] = value
}