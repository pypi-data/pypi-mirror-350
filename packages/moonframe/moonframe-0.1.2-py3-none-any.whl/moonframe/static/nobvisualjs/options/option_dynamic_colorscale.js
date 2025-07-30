import { onFocus, view } from "../tools/tools_zoom.js"
import { circularText } from "../tools/tools_text.js"
import { addCustomColor, changeColorScale, changeSingleColInOrdinal, increaseColID } from "../tools/tools_colorscale.js"
import { findWorst } from "./option_performers.js"
import { HEIGHT, WIDTH } from "../settings.js"

/**
 * Option to add a select form to dynamically change the color scale
 * @param {*} root Packed data
 * @param {string} nameKey Key in the data for the name of the circle
 * @param {string} colorKey Key in the data for the color scale
 */
export function addSelectForm(root, nameKey, colorKey) {
    // option to add a select form
    const selector = d3.select("#scaleSelector")

    for (let key in root.data) {
        if (key != nameKey && key != "children" && key != colorKey) {
            selector.append("option").attr("value", key).html(key)
        }
    }
}

/**
 * Update SVG after modifying the color scale
 * /!\ WARNING /!\ use d.colorID : update attributes before calling
 */
export function updateSVG() {
    const svg = d3.select("#main")
    const k = HEIGHT / view[2]

    // change color on svg
    svg.selectAll("textPath").remove()
    svg.selectAll("circle")
        .attr("fill", d => d.children ? "white" : d.colorID)
        .attr("stroke", d => d.children ? d.colorID : "null")

    // text
    if (!onFocus.parent) { //root
        svg.selectAll("circle").each(d => { circularText(d) })
    }

    else {
        if (onFocus.children) {
            for (const child of onFocus.children) {
                circularText(child, [WIDTH / 2 - view[0], HEIGHT / 2 - view[1]])
            }
        }
        circularText(onFocus, [WIDTH / 2 - view[0], HEIGHT / 2 - view[1]])
    }
}

/**
 * To call when an event modifies the value of "colorKey". 
 * Change everything that is dependant on color key. 
 * @param {*} root Packed data. 
 * @param {*} node 
 * @param {string} colorKey Key in the data for color
 * @param {boolean} worstIsBiggest Worst performers is the biggest (True) or not (False)
 * @param {boolean} isLog Log scale (True) or linear (False)
 */
export function updateAll(root, node, colorKey, worstIsBiggest, isLog) {

    // change color scale
    const color = changeColorScale(root, colorKey, isLog)

    // change attributes values
    node.each(function (d) {
        d.valueID = d.data[colorKey]
        d.colorID = color(d.data[colorKey])
    })

    //update SVG
    updateSVG(node)

    // card 
    if (!onFocus.children) {
        const card = d3.select("#card")
        card.select("#card-header").style("background-color", onFocus.colorID)
    }

    // find worst
    findWorst(root, colorKey, worstIsBiggest, node)

    colorCustomizationListener(root, node, color, colorKey, worstIsBiggest, isLog)

}

/**
 * Listen for change of color scale.
 * @param {*} root 
 * @param {*} node 
 * @param {*} color 
 * @param {string} colorKey 
 * @param {boolean} worstIsBiggest 
 * @param {boolean} isLog 
 */
export function colorCustomizationListener(root, node, color, colorKey, worstIsBiggest = true, isLog = false) {

    d3.select("#legend").select("image").on("click", function (event, d) {
        increaseColID()
        updateAll(root, node, colorKey, worstIsBiggest, isLog)
    })

    d3.select("#legend").select("g").selectAll("rect")
        .on("click", function (event, d) {
            const selection = d3.select(this)
            let currentColor = selection.style("fill")
            const colorPicker = document.getElementById("colorPicker")

            const y = event.pageY - document.getElementById("posColor").getBoundingClientRect().y - 10
            colorPicker.style.top = `${y}px`

            Coloris({
                el: '#colorPicker',
                theme: 'polaroid',
                defaultColor: currentColor,
                alpha: false,
                onChange: (newColor) => {
                    let index = d3.selectAll("#legend g rect").nodes().indexOf(this)
                    selection.style("fill", newColor)
                    changeSingleColInOrdinal(color, index, newColor)
                    // change attributes values 
                    node.each(function (d) {
                        d.valueID = d.data[colorKey]
                        d.colorID = color(d.data[colorKey])
                    })

                    updateSVG()
                    addCustomColor(colorKey, color)
                }
            });

            colorPicker.value = currentColor
            colorPicker.click()
        })

}

/* -------------------------------- LOG SCALE ------------------------------- */

/**
 * Option to add Log checkbox in the graph
 */
export function addLogCheckbox() {
    d3.select(".form-check").attr("hidden", null)
}

/**
 * Event listener : change of scale (log <-> linear)
 * @param {*} root 
 * @param {string} colorKey Key in the data for the color scale
 * @param {string} isLog Log scale (True) or linear (False)
 */
export function linearOrLog(root, colorKey, isLog) {
    const log10_checkbox = document.getElementById("log10_checkbox")

    log10_checkbox.addEventListener("change", function () {
        if (this.checked) {
            isLog = true
            changeColorScale(root, colorKey, isLog)
        } else {
            isLog = false
            changeColorScale(root, colorKey, isLog)
        }
    })
}