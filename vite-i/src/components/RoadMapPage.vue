<script setup>
import { ref, onMounted, watch } from 'vue';
// Import the actual Vue Flow diagram component
import RoadMapFlowchart from './RoadMapFlowchart.vue';
import Navbar from './Navbar.vue';

// Define props to receive user input from the router
const props = defineProps({
  userInput: {
    type: Object,
    default: () => ({ prompt: '' })
  }
});

// --- STATE MANAGEMENT ---
const isLoading = ref(false); // To show a loading state on the button
const showLoadingOverlay = ref(false); // full-screen loading overlay
const error = ref(null); // To display any errors from the API call

// VUE NODES - Initial state for the flowchart nodes
const nodes = ref([
  // main 3 nodes
  {
    id: '1',
    type: 'input',
    position: { x: 400, y: 40 },
    data: { label: 'PROGRAM' },
    class: 'primary', 
  },
  {
    id: '2',
    position: { x: 400, y: 190 },
    data: { label: 'PREREQUISITES' },
    class: 'primary',
  },
  {
    id: '3',
    position: { x: 400, y: 340 },
    data: { label: 'SCHOOL A' },
    class: 'primary', 
  },
  // sub-nodes of Prequisites (id: 2)
  {
    id: '4',
    type: 'output',
    position: { x: 200, y: 120 },
    data: { label: 'HI' },
    class: 'second'
  },
  {
    id: '5',
    type: 'output',
    position: { x: 200, y: 200 },
    data: { label: 'HELLO' },
    class: 'second'
  },
  {
    id: '6',
    type: 'output',
    position: { x: 200, y: 280 },
    data: { label: 'HEYO' },
    class: 'second'
  },
  {
    id: '7',
    type: 'output',
    position: { x: 600, y: 120 },
    data: { label: 'BYE' },
    class: 'second'
  },
  {
    id: '8',
    type: 'output',
    position: { x: 600, y: 200 },
    data: { label: 'GOODBYE' },
    class: 'second'
  },
  {
    id: '9',
    type: 'output',
    position: { x: 600, y: 280 },
    data: { label: 'SEE YA!' },
    class: 'second'
  },
  // school sub-nodes (id: 3)
  {
    id: '10',
    position: { x: 205, y: 420 },
    data: { label: 'Chill' },
    class: 'second'
  },
  {
    id: '11',
    position: { x: 400, y: 420 },
    data: { label: 'Cool' },
    class: 'second'
  },
  {
    id: '12',
    position: { x: 595, y: 420 },
    data: { label: 'Ice' },
    class: 'second'
  },
  // description of school sub-nodes (10 -> 13, 11 -> 14, 12 -> 15)
  {
    id: '13',
    type: 'output',
    position: { x: 205, y: 500 },
    data: { label: 'Hot' },
    class: 'second'
  },
  {
    id: '14',
    type: 'output',
    position: { x: 400, y: 500 },
    data: { label: 'Heat' },
    class: 'second'
  },
  {
    id: '15',
    type: 'output',
    position: { x: 595, y: 500 },
    data: { label: 'Fire' },
    class: 'second'
  },
]);

// --- SECURE API KEY HANDLING ---
// The Canvas environment automatically provides the API key, so leave it as an empty string.
const apiKey = "";

// --- GEMINI API INTEGRATION ---
/**
 * Main function to trigger the API call and update the node labels.
 * @param {string} userPrompt - The specific prompt from the user for roadmap generation.
 */
async function generateRoadmap(userPrompt = '') {
    isLoading.value = true;
    showLoadingOverlay.value = true; // Show the overlay
    error.value = null;

    try {
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

        // Combine the fixed context with the user's specific prompt
        const fullPrompt = `
          Here is the current structure of a flowchart with placeholder labels.
          The flowchart represents a personalized learning and career roadmap for a user in Cebu City, Philippines.
          The main nodes are 'PROGRAM', 'PREREQUISITES', and 'SCHOOL A'.
          The other nodes should be sub-topics or details related to these main nodes.
          Current labels: ${JSON.stringify(nodes.value.map(n => ({id: n.id, label: n.data.label})))}

          User's specific request: ${userPrompt}

          Based on the provided flowchart structure and the user's request, generate relevant and specific labels for EACH of the provided node IDs.
          For the 'PROGRAM' node (id: 1), suggest a specific tech-related degree (e.g., "BS in Information Technology").
          For the 'PREREQUISITES' node (id: 2), provide a high-level category (e.g., "Core Competencies").
          For the 'SCHOOL A' node (id: 3), name a specific, well-known university in Cebu that offers the suggested program (e.g., "University of San Carlos").
          The other nodes should be filled with related sub-topics, skills, or career steps.
          Return the response ONLY as a JSON array of objects, where each object has an "id" and a "newLabel", validating against the provided schema.
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
                parts: [{ text: fullPrompt }]
            }],
            systemInstruction: {
              parts: [{
                text: `You are a helpful career and education advisor for a user in Cebu City, Philippines. Your task is to populate a flowchart with a personalized roadmap.`
              }]
            },
            generationConfig: {
              responseMimeType: 'application/json',
              responseSchema: schema,
              temperature: 0.8,
            }
        };

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error?.message || 'Failed to fetch data from Gemini API.');
        }

        const data = await response.json();
        const newLabelsText = data.candidates && data.candidates.length > 0 &&
                             data.candidates[0].content && data.candidates[0].content.parts &&
                             data.candidates[0].content.parts.length > 0 ?
                             data.candidates[0].content.parts[0].text : null;


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
        console.error("Error generating roadmap:", e);
        error.value = e.message;
    } finally {
        isLoading.value = false;
        showLoadingOverlay.value = false; // Hide the overlay regardless of success or failure
    }
}

// Automatically generate roadmap when the component mounts or userInput changes
onMounted(() => {
  if (props.userInput && props.userInput.prompt) {
    generateRoadmap(props.userInput.prompt);
  }
});

watch(() => props.userInput.prompt, (newPrompt, oldPrompt) => {
  if (newPrompt && newPrompt !== oldPrompt) {
    generateRoadmap(newPrompt);
  }
});


const handleNavigateToHome = () => {
    // Implement navigation logic if needed
    console.log("Navigating to home from Roadmap page (placeholder)");
};

</script>

<template>
  <Navbar @navigateToHome="handleNavigateToHome"/>
  <div class="min-h-screen" style="background-color: #14161a;">
    <div
      :class="{ 'blur-sm': showLoadingOverlay, 'pointer-events-none': showLoadingOverlay }"
      class="flex-grow flex flex-col items-center p-6 pt-5 text-center transition-all duration-300 ease-out"
    >

      <div class="max-w-4xl mx-auto">
        <h2 class="text-4xl md:text-5xl font-bold mb-6 text-yellow-500 [text-shadow:0_0_10px_#FFD700] pt-6">Your Personalized Roadmap</h2>
        <p class="text-lg md:text-xl mb-12" style="color: #d2c179">
          Here's the AI-generated learning and career path tailored just for you. Located in Cebu City, Central Visayas, Philippines, we provide insights relevant to your region.
          <span v-if="props.userInput.prompt">
            Based on your request: "{{ props.userInput.prompt }}"
          </span>
        </p>
      </div>

      <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
        <strong>Error:</strong> {{ error }}
      </div>

      <RoadMapFlowchart :nodes="nodes"/>
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
        <button
            @click="generateRoadmap(props.userInput.prompt)"
            :disabled="isLoading"
            class="px-8 py-4 rounded-lg font-semibold text-black bg-gradient-to-r from-yellow-400 to-yellow-300 hover:bg-yellow-300 hover:text-black transition-colors focus:outline-none focus:ring-2 focus:ring-yellow-500">
            
            <span v-if="isLoading" class="flex items-center justify-center">
            <svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            Generating...
            </span>
             <span v-else>Regenerate Roadmap</span>
            </button>
      </div>
    </div>

    <transition name="fade">
      <div v-if="showLoadingOverlay" class="fixed inset-0 flex items-center justify-center z-50 backdrop-blur-sm" style="background-color: rgba(0, 0, 0, 0.7);">
        <div class="text-center">
          <img src="/loading.gif" alt="Loading" class="w-32 h-32 object-contain mx-auto mb-4 animate-pulse">
          <p class="text-yellow-400 text-xl font-semibold">Regenerating your personalized roadmap...</p>
        </div>
      </div>
    </transition>
    <div
            ref="whythis"
            class="max-w-2xl mx-auto p-6 rounded-2xl border-2 transition-shadow duration-500"
            :class="{ 'ring-4 ring-yellow-400': isHighlighted }"
            style="border-color: #FFD700; background-color: #ffd7000d;">
            <h2 class="text-2xl font-bold mb-6 bg-gradient-to-r from-yellow-500 to-yellow-200 bg-clip-text text-transparent">Roadmap Details</h2>

    <div class="mb-4">
        <ul class="list-none space-y-6"> <li>
        <div class="flex items-center space-x-2 mb-2"> <div class="w-3 h-3 rounded-full" style="background-color: #FFD700;"></div>
        <span style="color: #D2C179;">Suggested Program:</span>
        </div>
        <p class="ml-5" style="color: #FFF3C2;">hgsdfds</p> </li>
        <li>
        <div class="flex items-center space-x-2 mb-2"> <div class="w-3 h-3 rounded-full" style="background-color: #FFD700;"></div>
        <span style="color: #D2C179;">Suggested Program:</span>
        </div>
        <p class="ml-5" style="color: #FFF3C2;">hgsdfds</p> </li>
      
    </ul>
</div>
          </div>
  </div>
</template>

<style>
/* Import the necessary Vue Flow styles */
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/theme-default.css';

/* Existing styles for fade transition and blur */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.blur-sm {
  transition: filter 0.3s ease-out;
}
</style>