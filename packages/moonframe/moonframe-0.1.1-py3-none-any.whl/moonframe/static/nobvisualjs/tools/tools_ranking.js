/**
 * Sort files according to a key (rankKey)
 * @param {string} rankKey Sorting key
 * @param {boolean} worstIsBiggest Worst performers are the biggest (True) or the smallest (False)
 */
export function createRanking(root, rankKey, worstIsBiggest) {
    // takes only files
    const files = root.descendants().filter(d => !d.children)
    let ranking

    if (worstIsBiggest) { // ascending order (= worst file is in first pos)
        ranking = files.sort((a, b) => b.data[rankKey] - a.data[rankKey])
    }
    else { // descending order (= worst file is in last pos)
        ranking = files.sort((a, b) => a.data[rankKey] - b.data[rankKey])
    }

    return ranking
}