import * as d3 from "https://esm.sh/d3@7";

export default {
    initialize({ model }) {
        ;
    },
    render({ model, el }) {
        const width = 600;
        const height = width;

        console.log("Entering JS");

        // Clear previous content (important for AnyWidget re-rendering)
        el.innerHTML = '';

        // Create the main wrapper
        const wrapper = d3.select(el)
            .append('div')
            .attr('class', 'svg-button-wrapper');

        // Create the SVG element
        const svg = wrapper.append('svg')
            .attr('width', width)
            .attr('height', height);

        // Add groups to the SVG
        svg.append('g').attr('id', 'link-container');
        svg.append('g').attr('id', 'circle-container');

        // Create the button container
        const buttonContainer = wrapper.append('div')
            .attr('class', 'button-container');

        // Add buttons to the button container
        const buttons = [
            { id: 'must-link-button', textOne: 'Must-link', textTwo: '⬤━━━━━━━━━━━⬤' },
            { id: 'cannot-link-button', textOne: 'Cannot-link', textTwo: '⬤╸━╺╸━╺╸━╺╸━⬤' },
            { id: 'reset-button', textOne: 'Reset links', textTwo: '✖━━━━━⬤╸━╺╸━✖' }
        ];

        buttons.forEach(({ id, textOne, textTwo }) => {
            const button = buttonContainer.append('button')
                .attr('class', 'btn')
                .attr('id', id);

            button.append('span')
                .attr('class', 'btn-text-one')
                .text(textOne);

            button.append('span')
                .attr('class', 'btn-text-two')
                .text(textTwo);
        });

        const container = svg.select('#circle-container');
        const linkContainer = svg.select('#link-container');

        const dfIndices = model.get('df_indices');
        let textLabels = model.get('text_labels');
        if (textLabels.length != dfIndices.length)
            textLabels = Array(dfIndices.length).fill('');

        let n = dfIndices.length;
        const radius = width * 0.3; // Radius of the larger circle
        const centerX = width / 2;
        const centerY = height / 2;

        let graph = {
            nodes: dfIndices.map((dfIndex, i) => {
                const angle = i * (2 * Math.PI / n);
                return {
                    id: i,
                    dfIndex: dfIndex,
                    textLabel: textLabels[i],
                    x: centerX + radius * Math.cos(angle),
                    y: centerY + radius * Math.sin(angle)
                };
            }),
            mustLinks: [],
            cannotLinks: []
        };

        // Initialize disjoint sets
        const parent = Array.from({ length: n }, (_, i) => i);

        // Modified find function
        function find(x) {
            let root = x;
            while (parent[root] !== root) {
                root = parent[root];
            }
            // Path compression
            let current = x;
            while (current !== root) {
                let next = parent[current];
                parent[current] = root;
                current = next;
            }
            return root;
        }

        // Union function for union-find
        function union(x, y) {
            parent[find(y)] = find(x);
        }

        function removeFromMustLinkClique(nodeId) {

            parent[nodeId] = nodeId;

            // Find all nodes whose parent ID is nodeId
            const nodesWithParent = container.selectAll('circle').data().filter(node => parent[node.id] === nodeId && node.id !== nodeId);
            if (nodesWithParent.length === 0) return; // If no nodes with the given parentId, do nothing
            // Use the first node as the new parent for all other nodes with the same parentId
            const firstNode = nodesWithParent[0];
            // For each node with parentId = nodeId
            nodesWithParent.forEach(node => {
                parent[node.id] = firstNode.id; // Set the first node as the new parent for all other nodes
            });
        }

        // Create circles for nodes
        const circles = container.selectAll('circle')
            .data(graph.nodes)
            .enter().append('circle')
            .attr('cx', d => d.x)
            .attr('cy', d => d.y)
            .style('cursor', 'pointer')
            .on('click', function (event, d) {
                d3.select(this).classed('selected', !d3.select(this).classed('selected'));
            });

        // Add text labels for each node
        const labelContainer = container.selectAll('text')
            .data(graph.nodes)
            .enter().append('text')
            .attr('x', d => d.x)
            .attr('y', d => d.y - 16)
            .attr('text-anchor', 'middle') // Center-align the text
            .style('font-size', '14px') // Font size
            .style('pointer-events', 'none') // Ensure labels don't interfere with interaction
            .style('stroke', 'white') // Border color for the shadow effect
            .style('stroke-width', '2px') // Thickness of the shadow
            .style('paint-order', 'stroke') // Ensure the stroke is painted before the fill
            .style('fill', 'black') // Main text color
            .text(d => d.textLabel || '');



        let simulation;

        // Initialize or restart the force simulation
        function startSimulation() {
            if (simulation) simulation.stop();

            simulation = d3.forceSimulation(graph.nodes)
                .force('link', d3.forceLink(graph.mustLinks).id(d => d.id).distance(50))
                .force('charge', d3.forceManyBody().strength(-100))
                .force('center', d3.forceCenter(centerX, centerY))
                .force('circular', d3.forceRadial(radius).x(centerX).y(centerY))
                .force('bounds', () => {
                    graph.nodes.forEach(node => {
                        node.x = Math.max(10, Math.min(width - 10, node.x));
                        node.y = Math.max(10, Math.min(height - 10, node.y));
                    });
                })
                .on('tick', ticked);
        }

        function ticked() {
            circles.attr('cx', d => d.x)
                .attr('cy', d => d.y);

            labelContainer.attr('x', d => d.x)
                .attr('y', d => d.y - 15)

            linkContainer.selectAll('.must-link')
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);

            linkContainer.selectAll('.cannot-link')
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
        }

        function redistributeNodes() {
            const cliques = {};

            // Group nodes by their clique
            graph.nodes.forEach(node => {
                const root = find(node.id);
                if (!cliques[root]) cliques[root] = [];
                cliques[root].push(node);
            });

            const totalCliques = Object.keys(cliques).length;
            let angleOffset = 0;

            // Assign positions for each clique
            Object.values(cliques).forEach((clique, index) => {
                const cliqueAngle = (2 * Math.PI) / totalCliques;
                const startAngle = angleOffset;
                const endAngle = startAngle + cliqueAngle;

                clique.forEach((node, i) => {
                    const angle = startAngle + (i / clique.length) * (endAngle - startAngle);
                    node.x = centerX + radius * Math.cos(angle);
                    node.y = centerY + radius * Math.sin(angle);
                });

                angleOffset += cliqueAngle;
            });
        }

        function updateLinks() {
            let mustLinks = linkContainer.selectAll('.must-link')
                .data(graph.mustLinks, d => `${d.source.id}-${d.target.id}`);

            mustLinks.exit().remove();

            mustLinks.enter().append('line')
                .attr('class', 'must-link');

            mustLinks.merge(linkContainer.selectAll('.must-link'))
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);

            let cannotLinks = linkContainer.selectAll('.cannot-link')
                .data(graph.cannotLinks, d => `${d.source.id}-${d.target.id}`);

            cannotLinks.exit().remove();

            cannotLinks.enter().append('line')
                .attr('class', 'cannot-link');

            cannotLinks.merge(linkContainer.selectAll('.cannot-link'))
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
        }

        function deselectSelectionAndUpdateVis(selectedCircles) {
            selectedCircles.classed('selected', false);
            updateLinkConstraints();
            updateLinks();
            redistributeNodes();
            startSimulation();
        }

        function updateLinkConstraints() {
            const cliques = {};

            // Group nodes by their clique
            graph.nodes.forEach(node => {
                const root = find(node.id);
                if (!cliques[root]) cliques[root] = [];
                cliques[root].push(node);
            });

            let mustLinkConstraints = [];
            Object.values(cliques).forEach(clique => {
                let newMustLinkConstraint = [];
                if (clique.length > 1) {
                    clique.forEach(node => newMustLinkConstraint.push(node.dfIndex));
                    mustLinkConstraints.push(newMustLinkConstraint);
                }
            });

            let cannotLinkConstraints = [];
            graph.cannotLinks.forEach(cannotLink => {
                cannotLinkConstraints.push([cannotLink.source.dfIndex, cannotLink.target.dfIndex]);
            });

            // Update the widget model with the new constraints
            model.set('must_link_constraints', mustLinkConstraints);
            model.set('cannot_link_constraints', cannotLinkConstraints);

            // Ensure the model is updated in the frontend
            model.save_changes();
        }


        wrapper.select("#must-link-button").on('click', function () {
            console.log("Must-link button clicked");
            const selectedCircles = container.selectAll('.selected');

            if (selectedCircles.size() >= 2) {
                const selectedNodes = selectedCircles.data();

                // Union the sets of selected nodes
                selectedNodes.forEach((sourceNode, i) => {
                    selectedNodes.slice(i + 1).forEach(targetNode => {
                        union(sourceNode.id, targetNode.id);
                    });
                });

                // Remove cannot-links
                selectedNodes.forEach((sourceNode, i) => {
                    selectedNodes.slice(i + 1).forEach((targetNode, j) => {
                        if (find(sourceNode.id) === find(targetNode.id)) {
                            // Check if the cannotLink already exists
                            const existingLinkIndex = graph.cannotLinks.findIndex(link =>
                                (link.source === sourceNode && link.target === targetNode) ||
                                (link.source === targetNode && link.target === sourceNode)
                            );

                            // If the link exists, remove it
                            if (existingLinkIndex !== -1) {
                                graph.cannotLinks.splice(existingLinkIndex, 1); // Remove the link from cannotLinks
                            }
                        }
                    });
                });

                // Update must-links based on current cliques
                graph.mustLinks = [];
                for (let i = 0; i < graph.nodes.length; i++) {
                    for (let j = i + 1; j < graph.nodes.length; j++) {
                        if (find(i) === find(j)) {
                            graph.mustLinks.push({
                                source: graph.nodes[i],
                                target: graph.nodes[j]
                            });
                        }
                    }
                }

                deselectSelectionAndUpdateVis(selectedCircles);
            }
        });

        wrapper.select("#cannot-link-button").on('click', function () {
            console.log("Cannot-link button clicked");
            const selectedCircles = container.selectAll('.selected');

            if (selectedCircles.size() >= 2) {
                const selectedNodes = selectedCircles.data();

                // Initialize an empty list to store node IDs
                let nodesToRemove = [];

                // Iterate through selected nodes to find those in the same clique
                selectedNodes.forEach((sourceNode, i) => {
                    selectedNodes.slice(i + 1).forEach(targetNode => {
                        if (find(sourceNode.id) === find(targetNode.id)) {
                            // Add sourceNode.id and targetNode.id to the list if not already present
                            if (!nodesToRemove.includes(sourceNode.id)) {
                                nodesToRemove.push(sourceNode.id);
                            }
                            if (!nodesToRemove.includes(targetNode.id)) {
                                nodesToRemove.push(targetNode.id);
                            }
                        }
                    });
                });

                // Now remove nodes from cliques using the list of nodes
                nodesToRemove.forEach(nodeId => {
                    removeFromMustLinkClique(nodeId);
                });

                // Update must-links based on current cliques
                graph.mustLinks = [];
                for (let i = 0; i < graph.nodes.length; i++) {
                    for (let j = i + 1; j < graph.nodes.length; j++) {
                        if (find(i) === find(j)) {
                            graph.mustLinks.push({
                                source: graph.nodes[i],
                                target: graph.nodes[j]
                            });
                        }
                    }
                }

                // Add cannot-links
                selectedNodes.forEach((sourceNode, i) => {
                    selectedNodes.slice(i + 1).forEach(targetNode => {
                        // Check if the cannotLink already exists
                        const existingLink = graph.cannotLinks.some(link =>
                            (link.source === sourceNode && link.target === targetNode) ||
                            (link.source === targetNode && link.target === sourceNode)
                        );
                        // Only push if the cannotLink does not already exist
                        if (!existingLink) {
                            graph.cannotLinks.push({ source: sourceNode, target: targetNode });
                        }
                    });
                });

                deselectSelectionAndUpdateVis(selectedCircles);
            }
        });

        wrapper.select("#reset-button").on('click', function () {
            console.log("Reset button clicked");
            let selectedCircles = container.selectAll('.selected');

            if (selectedCircles.size() === 0) {
                // If no nodes are selected, treat all nodes as selected
                selectedCircles = container.selectAll('circle');
            }

            const selectedNodes = selectedCircles.data();

            // Reset parent for selected nodes
            selectedNodes.forEach(node => {
                removeFromMustLinkClique(node.id);
            });

            // Remove all links involving selected nodes
            graph.mustLinks = graph.mustLinks.filter(link =>
                !selectedNodes.includes(link.source) && !selectedNodes.includes(link.target)
            );

            graph.cannotLinks = graph.cannotLinks.filter(link =>
                !selectedNodes.includes(link.source) && !selectedNodes.includes(link.target)
            );

            deselectSelectionAndUpdateVis(selectedCircles);
        });

        startSimulation();
    }
};