import { HEIGHT, WIDTH, addSubtitle } from "./settings.js"
import { createColorScale } from "./tools/tools_colorscale.js"
import { addPerformersList } from "./options/option_performers.js"
import { circularText } from "./tools/tools_text.js"
import { zoom, setInitialView } from "./tools/tools_zoom.js"
import { Search as search } from "./tools/tools_search.js"
import { colorCustomizationListener, addSelectForm, addLogCheckbox, linearOrLog, updateAll } from "./options/option_dynamic_colorscale.js"
import { createCard } from "./options/option_cards.js"
import { openCode } from "./options/option_interactions.js"
import { setCircles } from "./tools/tools_svg.js"

/**
 * Create a new circle packing from data.
 * see https://d3js.org/d3-hierarchy/ for more documentation...
 * @param {*} data Nested data. Must contain a "children" key.
 * @returns Packed data
*/
function formatData(data, sizeBy) {

    const pack = d3.pack()
        .size([WIDTH, HEIGHT])
        .padding(WIDTH * 0.005)

    // Hierarchy -> flattened the structure
    const tree = d3.hierarchy(data)
        .sum(d => d[sizeBy])

    // Pack the package -> set coordinates and radius of each circles
    const root = pack(tree)

    return root
}

/* -------------------------------------------------------------------------- */
/*                              MAIN NOBVISUALJS                              */
/* -------------------------------------------------------------------------- */

/**
 * Basic nobvisual js graph with :
 *      - a title
 *      - a custom color scale
 *      - a tooltip
 *          
 * @param {*} data nested data. Must contain a "children" key.
 * @param {string} title title of the graph
 * @param {Object} legend (optional) custom color scale. Default to "undefined".
 * @param {string} colorKey key in the data for the color. Default to "color".
 * @param {string} sizeKey key in the data for the size. Default to "datum".
 * @param {string} nameKey key in the data for the name. Default to "text".
 * @returns 
 */
export function staticNobvisualjs(data,
    title,
    legend = undefined,
    colorKey = "color",
    sizeKey = "datum",
    nameKey = "text") {

    const root = formatData(data, sizeKey)
    let color = createColorScale(root, colorKey, legend)
    // set main attributes
    root.each(function (d, i) {
        d.ID = i
        d.nameID = d.data[nameKey]
        if (legend) {
            d.colorID = d.data[colorKey]
            d.valueID = legend[d.data[colorKey]]
        }
        else {
            d.colorID = color(d.data[colorKey])
            d.valueID = d.data[colorKey]
        }
    })
    const node = setCircles(root, color, colorKey)
    setInitialView(root, node)
    // assign name label following the curve
    node.each(d => { circularText(d) })
    document.getElementById("repo-name").innerHTML = title
    search(root, node)
    return [root, node, color]
}


/* -------------------------------------------------------------------------- */
/*                     MAIN NOBVISUALJS WITH CUSTOMIZATION                    */
/* -------------------------------------------------------------------------- */

/**
 * Main function dynamic Nobvisual js. Same as static nobvisual but with :
 *      - dynamic color scale (based on keys in the data) with log/linear option.
 *      - Card event to show more information
 *      - Performers list 
 * IMPORTANT : by definition, you can't use directly a custom color scale.
 * 
 * @param {*} data Nested data.
 * @param {string} title Title of the graph.
 * @param {string} colorKey Key in the data for the color scale.
 * @param {string} sizeKey Key in the data for the size of the circles.
 * @param {string} nameKey Key in the data for the name of the circles.
 * @param {string} idKey Key in the data for the id
 * @param {string} path Local path to repo
 */
export function dynamicNobvisualjs(data, title, path = "", colorKey = "NLOC", sizeKey = "NLOC", nameKey = "name") {

    let worstIsBiggest = true
    let isLog = false


    const [root, node, color] = staticNobvisualjs(data, title, undefined, colorKey, sizeKey, nameKey)

    // add & listeners
    addLogCheckbox()
    linearOrLog(root, colorKey, isLog)
    addSelectForm(root, nameKey, colorKey)
    addPerformersList(root, colorKey, worstIsBiggest, node)
    colorCustomizationListener(root, node, color, colorKey)
    // overloading click event to add feature
    d3.selectAll("circle").on("click", (event, d) => {
        if (event.metaKey || event.ctrlKey) {
            openCode(event, d, root, path)
        }
        else {
            zoom(d, root, node, HEIGHT)
            !d.children && createCard(root, d, nameKey, colorKey, worstIsBiggest)
        }
    })

    // EVENT

    // checkbox
    const log10_checkbox = document.getElementById("log10_checkbox")
    log10_checkbox.addEventListener("change", function () {
        if (this.checked) {
            isLog = true
            updateAll(root, node, colorKey, worstIsBiggest, isLog)
        } else {
            isLog = false
            updateAll(root, node, colorKey, worstIsBiggest, isLog)
        }
    })

    // select
    const select = document.querySelector(".form-select")
    select.addEventListener("change", function () {
        colorKey = select.value
        updateAll(root, node, colorKey, worstIsBiggest, isLog)
    })

}