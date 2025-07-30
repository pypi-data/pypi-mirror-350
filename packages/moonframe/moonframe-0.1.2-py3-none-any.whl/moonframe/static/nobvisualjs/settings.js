export const WWIDTH = window.innerWidth
export const WHEIGHT = window.innerHeight

// const WIDTH = WWIDTH
export const WIDTH = document.querySelector("#main").clientWidth
// const HEIGHT = WWIDTH - 50
export const HEIGHT = document.querySelector("#main").clientHeight * 3

/**
 * Add subtitle
 * @param {string} text Subtitle text
 */
export function addSubtitle(text) {
    const subtitle = d3.select("#subtitle")
    subtitle.html(text)
}

