import { focusOnElement } from "./tools_zoom.js"
/**
 * Run a search
 * @param {*} root Packed data
 * @param {*} node Circles data
 */
export function Search(root, node) {
    const searchInput = document.getElementById("searchInput")
    const infosearchtext = document.getElementById("info-search-text")
    const multiresult = document.getElementById("multiresults")

    // reboot
    document.addEventListener("click", function () {
        infosearchtext.innerHTML = ""
        searchInput.className = "form-control"
    })

    // reboot everything
    searchInput.addEventListener("click", function () {
        multiresult.innerHTML = ''
        infosearchtext.innerHTML = ""
        searchInput.className = "form-control"
    })

    searchInput.addEventListener('keydown', function (event) {
        if (event.key === 13 || event.key === "Enter") {
            event.preventDefault()
            searchElement(event, root, node)
        }
    })
}


/**
 * Finds elements that match the search input
 * 3 cases : 
 *      - nothing is found -> error message
 *      - single match -> zoom in
 *      - 2+ matches -> create a new menu
 * @param {*} event Event
 * @param {*} root Packed data
 * @param {*} node Circle data
 */
function searchElement(event, root, node) {

    event.preventDefault() // IMPORTANT !! disable restart of the code

    const searchInput = document.getElementById('searchInput')
    const multiresult = document.getElementById("multiresults")
    const infosearchtext = document.getElementById("info-search-text")
    const span = document.getElementById("inputGroupPrepend3")
    const searchRect = searchInput.getBoundingClientRect()
    const searchTerm = searchInput.value
    // Find elements that match the search input.
    const matches = root.descendants().filter(d => d.nameID === searchTerm)

    multiresult.innerHTML = ""
    infosearchtext.innerHTML = ""
    searchInput.className = "form-control"

    if (matches.length !== 0) { // something found

        if (matches.length > 1) { // more than one match -> create a menu
            // placement
            span.insertAdjacentElement('afterend', multiresult)
            multiresult.style.position = `absolute`
            multiresult.style.top = `${searchRect.height}px`
            multiresult.style.minWidth = 150 // fake width -> place under search bar
            multiresult.style.maxWidth = 200
            span.style.borderRadius = `5px`

            // set list of buttons
            matches.forEach(d => {
                const option = document.createElement('button')
                option.className = 'btn btn-light'
                option.textContent = d.data.path
                option.onclick = () => { focusOnElement(d, event, root, node) }
                multiresult.appendChild(option)
            })
        }
        else { // single match
            focusOnElement(matches[0], event, root, node)
        }

    }
    else { // nothign found -> error message
        // placement
        span.insertAdjacentElement('afterend', infosearchtext)
        infosearchtext.style.position = `absolute`
        infosearchtext.style.top = `${searchRect.height}px`
        infosearchtext.style.minWidth = 500 // fake width -> place under search bar
        infosearchtext.innerHTML = `Can't find ${searchTerm}.`
        span.style.borderRadius = `5px`
        infosearchtext.style.textAlign = "left"
        infosearchtext.style.color = 'red'
        searchInput.className = "form-control is-invalid"
    }
    searchInput.value = ""
}
