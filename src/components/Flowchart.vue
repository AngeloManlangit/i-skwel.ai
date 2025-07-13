<script setup>
import { ref } from 'vue';
import { VueFlow } from '@vue-flow/core';

const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  }
})

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
    animated: 'true',
  },

  {
    id: 'e2->5',
    source: '2', 
    target: '5', 
    animated: 'true',
  },

  {
    id: 'e2->6',
    source: '2', 
    target: '6', 
    animated: 'true',
  },

  {
    id: 'e2->7',
    source: '2', 
    target: '7', 
    animated: 'true',
  },

  {
    id: 'e2->8',
    source: '2', 
    target: '8', 
    animated: 'true',
  },

  {
    id: 'e2->9',
    source: '2', 
    target: '9', 
    animated: 'true',
  },

  // school to school sub-nodes
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

  // school sub-nodes to desciption
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
    <!-- Vue Flow Diagram -->
    <div class="vue-flow-container" :style="{ height: '1000px', width: '100%' }">
        <VueFlow
            :nodes="props.nodes"
            :edges="edges"
            fit-view-on-init
            :paneMovable="false"  >
        </VueFlow>
    </div>
</template>

<style>
.vue-flow__node {
  font-family: 'Inter', sans-serif;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.vue-flow__node.default {
 
  background-color: #14181C;
  border-color: #333; 
  color: #D2C179;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.vue-flow__edge-path,
.vue-flow__connection-path {
  stroke: #FFD700;
}

.vue-flow__controls-button {
  background-color: #14181C;
  color: #FFD700;
  border: 1px solid #FFD700;
  margin: 4px;
}

.vue-flow__controls-button:hover {
  background-color: #20242a;
}

.vue-flow__minimap {
  background-color: #14161A;
  border: 1px solid #FFD700;
}

.vue-flow__minimap-node {
  fill: #FFD700;
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