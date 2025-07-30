import { createRanking } from "../tools/tools_ranking.js"
import { focusOnElement } from "../tools/tools_zoom.js"

/**
 * Add performers list to the graph
 * @param {*} root Packed data
 * @param {string} colorKey Key in the data for the color scale
 * @param {boolean} worstIsBiggest Worst performers are the biggest (True) or the smallest (False)
 * @param {*} node Circles data
 */
export function addPerformersList(root, colorKey, worstIsBiggest, node) {
    d3.select("#worst-title").attr("hidden", null)
    findWorst(root, colorKey, worstIsBiggest, node)
}

/**
 * Set the worst performers list
 * @param {*} root Packed data
 * @param {string} colorKey Key in the data for the color scale
 * @param {boolean} worstIsBiggest Worst performers are the biggest (True) or the smallest (False)
 * @param {*} node Circles data
 */
export function findWorst(root, colorKey, worstIsBiggest, node) {
    const worst = document.getElementById("worst")
    const ranking = createRanking(root, colorKey, worstIsBiggest)

    d3.select("#worst").selectAll("*").remove()

    if (!(typeof root.descendants()[0].data[colorKey] == "string")) {
        for (let i = 0; i < 10; i++) {
            if (ranking[i]) {
                const worst_el = document.createElement('a')
                worst_el.textContent = ranking[i].nameID
                worst_el.href = "#"
                worst_el.onclick = (event) => { focusOnElement(ranking[i], event, root, node) }
                worst.appendChild(worst_el)
            }
        }
    }
}