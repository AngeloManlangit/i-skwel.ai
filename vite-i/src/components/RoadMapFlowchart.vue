<script setup>
import { ref } from 'vue';
import { VueFlow } from '@vue-flow/core';


const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  }
})

// Define the edges for the flowchart
const edges = ref([
  {
    id: 'e1->2',
    source: '1',
    target: '2',
  },
  {
    id: 'e2->3',
    source: '2',
    target: '3',
  },
  // Prereq nodes to sub-nodes
  {
    id: 'e2->4',
    source: '2',
    target: '4',
    animated: true, // Use boolean true, not string 'true'
  },
  {
    id: 'e2->5',
    source: '2',
    target: '5',
    animated: true,
  },
  {
    id: 'e2->6',
    source: '2',
    target: '6',
    animated: true,
  },
  {
    id: 'e2->7',
    source: '2',
    target: '7',
    animated: true,
  },
  {
    id: 'e2->8',
    source: '2',
    target: '8',
    animated: true,
  },
  {
    id: 'e2->9',
    source: '2',
    target: '9',
    animated: true,
  },
  // School to school sub-nodes
  {
    id: 'e3->10',
    source: '3',
    target: '10',
  },
  {
    id: 'e3->11',
    source: '3',
    target: '11',
  },
  {
    id: 'e3->12',
    source: '3',
    target: '12',
  },
  // School sub-nodes to description
  {
    id: 'e10->13',
    source: '10',
    target: '13',
    animated: true,
  },
  {
    id: 'e11->14',
    source: '11',
    target: '14',
    animated: true,
  },
  {
    id: 'e12->15',
    source: '12',
    target: '15',
    animated: true,
  },
]);

</script>

<template>
  
    <!-- Vue Flow Diagram Container -->
    <div class="vue-flow-container" :style="{ height: '1000px', width: '80%' }">
        <VueFlow
            :nodes="props.nodes"
            :edges="edges"
            fit-view-on-init
            
            :paneMovable="false"
            :zoomOnScroll="false"   
            :zoomOnPinch="false"  
            :zoomOnDoubleClick="false" >
        </VueFlow>
    </div>
</template>

<style>
/* Styles for Vue Flow nodes and edges */
.vue-flow__node.default {
  background-color: #14181C;
  border-color: #333;
  color: #eedf00;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 8px 12px; /* Added padding for better text display */
}

/*
.vue-flow__node {
  font-family: 'Inter', sans-serif;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  border-radius: 8px; /Added rounded corners /
  background-color: #333;
  color: #eedf00;
}
*/
.vue-flow__node.primary {
    background-color: #332f2d;
    border-color: #eedf00;
    color: #FFD700; 
}

.vue-flow__node:hover {
  background-color: #383b42; 
  border-color: #e6e3d2; 
}

.vue-flow__edge-path,
.vue-flow__connection-path {
  stroke: #98cd10;
  stroke-width: 20px; /* Make edges slightly thicker */
}

.vue-flow__controls-button {
  background-color: #14181C;
  color: #FFD700;
  border: 1px solid #FFD700;
  margin: 4px;
  border-radius: 4px; /* Added rounded corners */
}

.vue-flow__controls-button:hover {
  background-color: #20242a;
}


.vue-flow__node.second{
  background-color: #332f2d;
  color: white;
  border-color: rgb(210, 185, 115);
}


.vue-flow__node.second:hover {
  background-color: #383b42; 
  border-color: #FFD700; 
}

.vue-flow__node-label {
  white-space: normal;
  word-break: break-word;
  max-width: 180px;
}

.vue-flow__pane {
  background-color: transparent !important;
}

</style>
