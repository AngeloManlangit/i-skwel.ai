<script setup>
import { ref } from 'vue';
import Flowchart from './components/Flowchart.vue';

// --- STATE MANAGEMENT ---
const isLoading = ref(false); // To show a loading state on the button
const error = ref(null); // To display any errors from the API call

// VUE NODES
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
    position: { x: 205, y: 550 },
    data: { label: 'Hot' },
  },

  { 
    id: '14',
    type: 'output',
    position: { x: 400, y: 550 },
    data: { label: 'Heat' },
  },

  { 
    id: '15',
    type: 'output',
    position: { x: 595, y: 550 },
    data: { label: 'Fire' },
  },
]);

// --- SECURE API KEY HANDLING ---
const apiKey = import.meta.env.VITE_GEMINI_API_KEY;

// --- GEMINI API INTEGRATION ---
/**
 * Main function to trigger the API call and update the node labels.
 */
async function generateRoadmap() {
    isLoading.value = true;
    error.value = null;

    if (!apiKey) {
        error.value = 'VITE_GEMINI_API_KEY is not defined in your .env file.';
        isLoading.value = false;
        return; // Exit early if no API key is found
    }

    try {
        const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=${apiKey}`;

        // Provide the model with the current node structure as context.
        const contextPrompt = `
          Here is the current structure of a flowchart with placeholder labels.
          The flowchart represents a personalized learning and career roadmap for a user in Cebu City, Philippines.
          The main nodes are 'PROGRAM', 'PREREQUISITES', and 'SCHOOL A'.
          The other nodes are sub-topics or details related to these main nodes.
          Current labels: ${JSON.stringify(nodes.value.map(n => ({id: n.id, label: n.data.label})))}
        `;

        // Define the JSON schema for the expected response.
        const schema = {
          type: 'ARRAY',
          items: {
            type: 'OBJECT',
            properties: {
              id: { type: 'STRING' },
              newLabel: { type: 'STRING' },
            },
            required: ['id', 'newLabel'],
          },
        };

        const requestBody = {
            contents: [{
                parts: [{ text: contextPrompt }]
            }],
            systemInstruction: {
              parts: [{
                text: `You are a helpful career and education advisor for a user in Cebu City, Philippines. Your task is to populate a flowchart with a personalized roadmap.
                Based on the provided flowchart structure, generate relevant and specific labels for EACH of the provided node IDs.
                For the 'PROGRAM' node (id: 1), suggest a specific tech-related degree.
                For the 'PREREQUISITES' node (id: 2), provide a high-level category (e.g., "Core Competencies").
                For the 'SCHOOL A' node (id: 3), name a specific, well-known university in Cebu that offers the suggested program.
                The other nodes should be filled with related sub-topics, skills, or career steps.
                Return the response ONLY as a JSON array of objects, where each object has an "id" and a "newLabel", validating against the provided schema.`
              }]
            },
            generationConfig: {
              responseMimeType: 'application/json',
              responseSchema: schema,
              temperature: 0.8,
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
        const newLabelsText = data.candidates[0]?.content?.parts[0]?.text;

        if (!newLabelsText) {
            throw new Error('Received an empty or invalid JSON response from the API.');
        }

        const parsedLabels = JSON.parse(newLabelsText);

        // Create a map for easy lookup
        const labelMap = new Map(parsedLabels.map(item => [item.id, item.newLabel]));

        // Update the nodes with the new labels from the map
        nodes.value = nodes.value.map(node => {
            if (labelMap.has(node.id)) {
                return {
                    ...node,
                    data: {
                        ...node.data,
                        label: labelMap.get(node.id),
                    }
                };
            }
            return node;
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
  <main class="min-h-screen bg-gradient-to-b from-gray-950 to-black">
    <section class="px-6 pt-32 text-white text-center">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-4xl md:text-5xl font-bold mb-6 text-yellow-400 [text-shadow:0_0_10px_#FFD700]">Your Personalized Roadmap</h2>
        <p class="text-lg md:text-xl text-gray-300 mb-12">
          Here's the AI-generated learning and career path tailored just for you. Located in Cebu City, Central Visayas, Philippines, we provide insights relevant to your region.
        </p>
      
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <button 
            @click="generateRoadmap" 
            :disabled="isLoading || !apiKey"
            class="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors duration-300 w-full sm:w-auto"
          >
            <span v-if="isLoading" class="flex items-center justify-center">
              <svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              Generating...
            </span>
            <span v-else>Generate Roadmap</span>
          </button>
          
          <img src="./assets/i-skwelai-anim2.gif" v-if="isLoading" class="z-1 fixed w-120 pt-50">
        </div>

        <!-- Error Message Display -->
        <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          <strong>Error:</strong> {{ error }}
        </div>
        <div v-if="!apiKey" class="mt-4 p-3 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded-lg">
          <strong>Warning:</strong> Your `VITE_GEMINI_API_KEY` is not set in your `.env` file. The button will be disabled.
        </div>

        <!-- Vue Flow Diagram -->
        <Flowchart :nodes="nodes"/>
      </div>
    </section>
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