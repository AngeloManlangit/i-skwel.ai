<script setup>
import { ref } from 'vue';
import { VueFlow } from '@vue-flow/core';

// --- STATE MANAGEMENT ---
const isLoading = ref(false); // To show a loading state on the button
const error = ref(null); // To display any errors from the API call

// --- SECURE API KEY HANDLING ---
// The API key is now read securely from the .env file.
// Vite exposes environment variables prefixed with VITE_ on the import.meta.env object.
const apiKey = import.meta.env.VITE_GEMINI_API_KEY;


// --- VUE FLOW NODES ---
const nodes = ref([

  // main 3 nodes
  { 
    id: '1',
    type: 'input', 
    position: { x: 400, y: 40 },
    // all nodes can have a data object containing any data you want to pass to the node
    // a label can property can be used for default nodes
    data: { label: 'PROGRAM' },
    class: 'bg-green-100 border-green-400',
  },

  { 
    id: '2',
    position: { x: 400, y: 190 },
    data: { label: 'PREREQUISITES' },
  },

  { 
    id: '3',
    position: { x: 400, y: 340 },
    data: { label: 'SCHOOL A' },
  },

  // sub-nodes of Prequisites (id: 2)
  { 
    id: '4',
    type: 'output',
    position: { x: 200, y: 120 },
    data: { label: 'HI' },
  },

  { 
    id: '5',
    type: 'output',
    position: { x: 200, y: 200 },
    data: { label: 'HELLO' },
  },

  { 
    id: '6',
    type: 'output',
    position: { x: 200, y: 280 },
    data: { label: 'HEYO' },
  },

  { 
    id: '7',
    type: 'output',
    position: { x: 600, y: 120 },
    data: { label: 'BYE' },
  },

  { 
    id: '8',
    type: 'output',
    position: { x: 600, y: 200 },
    data: { label: 'GOODBYE' },
  },

  { 
    id: '9',
    type: 'output',
    position: { x: 600, y: 280 },
    data: { label: 'SEE YA!' },
  },

  // school sub-nodes (id: 3)

  {
    id: '10',
    position: { x: 205, y: 420 },
    data: { label: 'Chill' },
  },

  {
    id: '11',
    position: { x: 400, y: 420 },
    data: { label: 'Cool' },
  },

  {
    id: '12',
    position: { x: 595, y: 420 },
    data: { label: 'Ice' },
  },

  // description of school sub-nodes (10 -> 13, 11 -> 14, 12 -> 15)
  { 
    id: '13',
    type: 'output',
    position: { x: 205, y: 500 },
    data: { label: 'Hot' },
  },

  { 
    id: '14',
    type: 'output',
    position: { x: 400, y: 500 },
    data: { label: 'Heat' },
  },

  { 
    id: '15',
    type: 'output',
    position: { x: 595, y: 500 },
    data: { label: 'Fire' },
  },
]);

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

// --- GEMINI API INTEGRATION ---
/**
 * Fetches a specified number of random words from the Gemini API.
 * @param {number} count - The number of random words to fetch.
 * @returns {Promise<string[]>} A promise that resolves to an array of words.
 */
async function fetchRandomWords(count = 5) {
    if (!apiKey) {
        throw new Error('VITE_GEMINI_API_KEY is not defined in your .env file.');
    }
    
    const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=${apiKey}`;
    
    const prompt = `Generate ${count} random English words that can be found in the Merriam-Webster dictionary, separated by commas. For example: "Cat,Tree,Book,Sun,River"`;

    const requestBody = {
        contents: [{
            parts: [{ text: prompt }]
        }],
        generationConfig: {
            temperature: 1.5,
        }
    };

    const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error?.message || 'Failed to fetch data from Gemini API.');
    }

    const data = await response.json();
    const text = data.candidates[0]?.content?.parts[0]?.text;

    if (!text) {
        throw new Error('Received an empty response from the API.');
    }

    return text.trim().split(',').map(word => word.trim());
}

/**
 * Main function to trigger the API call and update the node labels.
 */
async function fetchAndUpdateLabels() {
    isLoading.value = true;
    error.value = null;
    try {
        const wordsNeeded = nodes.value.filter(n => n.type !== 'input' && n.type !== 'output').length;
        const words = await fetchRandomWords(wordsNeeded);

        let wordCounter = 0;
        nodes.value = nodes.value.map((node) => {
            if (node.type === 'input' || node.type === 'output') {
                return node;
            }
            
            const newLabel = words[wordCounter] || `Node ${node.id}`;
            wordCounter++;
            
            return { ...node, label: newLabel };
        });

    } catch (e) {
        console.error(e);
        error.value = e.message;
    } finally {
        isLoading.value = false;
    }
}
</script>

<template>
  <main class="min-h-screen flex flex-col items-center justify-center p-4 bg-gray-800 font-sans">
    <div class="w-full max-w-4xl mx-auto">
      
        <!-- Button to trigger the fetch -->
        <div class="text-center">
          <button 
            @click="fetchAndUpdateLabels" 
            :disabled="isLoading || !apiKey"
            class="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors duration-300"
          >
            <span v-if="isLoading" class="flex items-center justify-center">
              <svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Fetching...
            </span>
            <span v-else>Get Random Labels</span>
          </button>
        </div>
        
        <!-- Error Message Display -->
        <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          <strong>Error:</strong> {{ error }}
        </div>
        <div v-if="!apiKey" class="mt-4 p-3 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded-lg">
          <strong>Warning:</strong> Your `VITE_GEMINI_API_KEY` is not set in your `.env` file. The button will be disabled.
        </div>

      <!-- Vue Flow Diagram -->
      <div class="w-full h-[80vh] bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
        <VueFlow :default-viewport="{ zoom: 1.3, position: { x: -100, y:0 } }" :nodes="nodes" :edges="edges">
          <Background />
        </VueFlow>
      </div>
    </div>
  </main>
</template>

<style>
/* Import the necessary Vue Flow styles */
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/theme-default.css';

/* Basic styles for the app layout */
body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* You can add custom styles for your nodes here if needed */
.vue-flow__node-input.bg-green-100 {
    background-color: #d1fae5;
    border-color: #6ee7b7;
}

.vue-flow__node-output.bg-red-100 {
    background-color: #fee2e2;
    border-color: #fca5a5;
}
</style>