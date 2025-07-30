import { isTransition, view } from "../tools/tools_zoom.js"
import { createRanking } from "../tools/tools_ranking.js"
import { HEIGHT } from "../settings.js"

/**
 * Create a card to show more information.
 * @param {*} root Packed data.
 * @param {*} d Selected circle.
 * @param {string} nameKey Key in the data for the name of the circles
 * @param {string} colorKey Key in the data for the color scale.
 * @param {boolean} worstIsBiggest Worst performers are the biggest (True) or the smallest (False)
 */
export function createCard(root, d, nameKey, colorKey, worstIsBiggest) {
    // option to add a card
    const card = d3.select("#card")
    const svg = d3.select("#main")
    const svgBounds = svg.node().getBoundingClientRect() // real size of node
    const cardBody = document.getElementById("element-card")

    /**
     * Set card coordinates after the zoom transition.
     */
    function VisibleAfterZoom() {
        if (isTransition) {
            setTimeout(VisibleAfterZoom, 50)
        }
        else {
            card.style("opacity", 1)
                .select("#card-header")
                .html(`${d.nameID}`)
                .style("background-color", d.colorID)
                .style("color", "white")

            // card.select("#card-text")
            //     .html(text)

            const k = HEIGHT / view[2]
            card.style("min-width", "150px")
            .style("max-width", "320px")
            // card.style("top", d.y - d.r * k)
            .style("left", (svgBounds.right - card.node().offsetWidth - 25+ "px"))
        }
    }

    cardBody.innerHTML = "" // reboot card
    //add data
    for (let key in d.data) {
        if (key != nameKey && key != "children") {
            // key name
            let row = document.createElement("div")
            row.className = "row"
            let keyname = document.createElement("div")
            keyname.className = "col"
            keyname.innerHTML = key
            keyname.style.fontWeight = "bold"
            keyname.style.textAlign = "left"
            keyname.style.maxWidth = "90px"
            row.appendChild(keyname)
            // score
            let score = document.createElement("div")
            score.className = "col"
            score.innerHTML = d.data[key]
            score.style.textAlign = "left"
            score.style.maxHeight = "20px"
            score.style.overflow = "hidden"
            score.style.textOverflow = "ellipsis"
            row.appendChild(score)
            // rank
            let rank = document.createElement("div")
            rank.className = "col"
            if (typeof d.data[key] === "string") {
                rank.innerHTML = ""

            }
            else {
                const ranking = createRanking(root, key, worstIsBiggest)
                if (ranking.slice(0, 10).includes(d)) {
                    rank.innerHTML = `<span class="badge text-bg-danger">BOTTOM 10</span>`
                }
                else if (ranking.slice(-10).includes(d)) {
                    rank.innerHTML = `<span class="badge text-bg-success">TOP 10</span>`
                }
                else {
                    rank.innerHTML = `<span class="badge text-bg-secondary">AVERAGE</span>`
                }
            }
            rank.style.textAlign = "left"
            row.appendChild(rank)
            cardBody.appendChild(row)

        }
    }
    VisibleAfterZoom()
}