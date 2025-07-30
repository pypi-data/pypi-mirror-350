/* ------------------------------- CTRL CLICK ------------------------------- */

/**
 * Open code in VSCode event
 * @param {*} event 
 * @param {*} d 
 * @param {string} path Local path to the repo
 */
export function openCode(event, d, root, path) {
    event.preventDefault()
    if (d.data.path.includes(":")) { // inside files
        const parent_path = d.data.path.split(":")[0]
        window.location.href = `vscode://file//${path}/${root.data.name}/${parent_path}:${d.data.lines[0]}`
    }
    else {
        window.location.href = `vscode://file//${path}/${root.data.name}/${d.data.path}`
    }
}
