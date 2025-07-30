/**
* Set the tooltip according to the circle selected
* A tooltip appears when you hover over a circle.
* @param {*} d Selected circle
* @param {*} event Event
*/
export function setTooltip(d, event) {
    const tooltip = d3.select("#tooltip")

    tooltip.style("left", event.pageX + 15 + "px")
    tooltip.style("top", event.pageY + 15 + "px")
    tooltip.style("opacity", 1)
        .select("#tooltip-title")
        .html(`${d.nameID}`)


    let d_value = d.valueID
    const bg_color = d.colorID
    tooltip.select("#tooltip-text")
        .html(function (d) {
            let text = `${d_value}`
            return text.replace(d_value, `<span style="background-color: ${bg_color};
                                                         color: white;
                                                         padding: 5px;
                                                         border-radius: 10px; 
                                                         display: inline-block ;">${d_value}</span>`)
        })
}
