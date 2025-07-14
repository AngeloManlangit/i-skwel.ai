<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router'; // Import useRoute
import RoadMapFlowchart from './RoadMapFlowchart.vue';
import Navbar from './Navbar.vue';

const route = useRoute(); // Initialize useRoute

// Define props (if any other props are needed, keep them here)
// Removed the userInput prop definition as we'll read directly from route.query
const props = defineProps({
  // If you have other props that are NOT from router query, define them here.
  // For now, assuming userInput was the only one.
});

// API URL
const BACKEND_API_URL = 'http://localhost:5000/generate_roadmap'

// --- STATE MANAGEMENT ---
const isLoading = ref(false); // To show a loading state on the button
const showLoadingOverlay = ref(false); // full-screen loading overlay
const error = ref(null); // To display any errors from the API call
const suggestedProgram = ref('');
const whyThisProgram = ref('');
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
    data: { label: 'RESOURCES' },
    class: 'primary',
  },
  {
    id: '3',
    position: { x: 400, y: 340 },
    data: { label: 'COLLEGES' },
    class: 'primary', 
  },
  // sub-nodes of Prequisites (id: 2)
  {
    id: '4',
    type: 'output',
    position: { x: 200, y: 120 },
    data: { label: 'RESOURCE1' },
    class: 'second'
  },
  {
    id: '5',
    type: 'output',
    position: { x: 200, y: 200 },
    data: { label: 'RESOURCE2' },
    class: 'second'
  },
  {
    id: '6',
    type: 'output',
    position: { x: 200, y: 280 },
    data: { label: 'RESOURCE3' },
    class: 'second'
  },
  {
    id: '7',
    type: 'output',
    position: { x: 600, y: 120 },
    data: { label: 'RESOURCE4' },
    class: 'second'
  },
  {
    id: '8',
    type: 'output',
    position: { x: 600, y: 200 },
    data: { label: 'RESOURCE5' },
    class: 'second'
  },
  {
    id: '9',
    type: 'output',
    position: { x: 600, y: 280 },
    data: { label: 'RESOURCE6' },
    class: 'second'
  },
  // school sub-nodes (id: 3)
  {
    id: '10',
    position: { x: 205, y: 420 },
    data: { label: 'SCHOOL1' },
    class: 'second'
  },
  {
    id: '11',
    position: { x: 400, y: 420 },
    data: { label: 'SCHOOL2' },
    class: 'second'
  },
  {
    id: '12',
    position: { x: 595, y: 420 },
    data: { label: 'SCHOOL3' },
    class: 'second'
  },
  // description of school sub-nodes (10 -> 13, 11 -> 14, 12 -> 15)
  {
    id: '13',
    type: 'output',
    position: { x: 205, y: 500 },
    data: { label: 'SCHOOL1_INFO' },
    class: 'second'
  },
  {
    id: '14',
    type: 'output',
    position: { x: 400, y: 500 },
    data: { label: 'SCHOOL2_INFO' },
    class: 'second'
  },
  {
    id: '15',
    type: 'output',
    position: { x: 595, y: 500 },
    data: { label: 'SCHOOL3_INFO' },
    class: 'second'
  },
]);

// --- SECURE API KEY HANDLING ---
const apiKey = import.meta.env.VITE_GEMINI_API_KEY;

// --- GEMINI API INTEGRATION ---
/**
 * Main function to trigger the API call and update the node labels.
 * @param {string} [userPrompt=null] - Optional user prompt to use for the API call.
 * If not provided, it falls back to route.query.prompt
 * or a default hardcoded query.
 */
async function generateRoadmap(userPrompt = null) {
  isLoading.value = true;
  error.value = null;
  showLoadingOverlay.value = true; // Ensure overlay is shown

  try {
    // --- DEBUGGING LOGS ---
    console.log("generateRoadmap called.");
    console.log("userPrompt argument:", userPrompt);
    console.log("route.query:", route.query); // Log route.query directly
    console.log("route.query.prompt:", route.query.prompt); // Log route.query.prompt
    // --- END DEBUGGING LOGS ---

    // Determine the actual user query to send to the backend
    // Now correctly using route.query.prompt
    const actualUserQuery = userPrompt || route.query.prompt || "I enjoy cooking. I want to pursue the art of cooking, and becomme a chef. Help me in my journey.";
    console.log("actualUserQuery determined:", actualUserQuery); // Add this too

    // Prepare the data to send to the backend
    // We send the current node structure and the user query/context.
    const requestBody = {
      // We pass the current nodes array structure and labels for context
      currentNodes: nodes.value.map(n => ({ id: n.id, label: n.data.label })),
      userQuery: actualUserQuery, // Use the determined user query
      // You might also want to send location and startingPoint if your backend uses them:
      location: route.query.location,
      startingPoint: route.query.startingPoint
    };

    const response = await fetch(BACKEND_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || 'Failed to fetch data from backend API.');
    }

    // The backend now returns the structured JSON array directly.
    // We do not need to parse JSON from response.text or look for 'candidates[0]'.
    const parsedLabels = await response.json(); 

    const programData = parsedLabels.find(item => item.id === '1');
    const whyData = parsedLabels.find(item => item.id === 'why-this-program');

    if (programData) {
      suggestedProgram.value = programData.newLabel;
    }
    if (whyData) {
      whyThisProgram.value = whyData.newLabel;
    }
    if (!parsedLabels || !Array.isArray(parsedLabels)) {
      throw new Error('Received an empty or invalid JSON array from the backend.');
    }

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
    error.value = e.message || 'An unknown error occurred.';
  } finally {
    isLoading.value = false;
    showLoadingOverlay.value = false; // Hide overlay when generation finishes
  }
}
// Automatically generate roadmap when the component mounts or route.query.prompt changes
onMounted(() => {
  // Use route.query.prompt directly
  if (route.query.prompt) {
    generateRoadmap(route.query.prompt);
  } else {
    // If no prompt from query, generate with default or initial state
    generateRoadmap(); 
  }
});

watch(() => route.query.prompt, (newPrompt, oldPrompt) => {
  if (newPrompt && newPrompt !== oldPrompt) {
    generateRoadmap(newPrompt);
  }
});

const handleNavigateToHome = () => {
    // Implement navigation logic if needed
    console.log("Navigating to home from Roadmap page (placeholder)");
};

defineExpose({
  generateRoadmap // Still expose if you intend to call it from parent components (e.g., for "Regenerate Roadmap" button)
});
</script>

<template>
  <div>
  <Navbar @navigateToHome="handleNavigateToHome"/>
  <div class="min-h-screen" style="background-color: #14161a;">
    <div
      :class="{ 'blur-sm': showLoadingOverlay, 'pointer-events-none': showLoadingOverlay }"
      class="flex-grow flex flex-col items-center p-6 pt-5 text-center transition-all duration-300 ease-out"
    >

      <div class="max-w-4xl mx-auto">
        <h2 class="text-4xl md:text-5xl font-bold mb-6 text-yellow-500 [text-shadow:0_0_10px_#FFD700] pt-6">Your Personalized Roadmap</h2>
        <p class="text-lg md:text-xl npm-12" style="color: #d2c179">
          Here's the AI-generated learning and career path tailored just for you. Located in Cebu City, Central Visayas, Philippines, we provide insights relevant to your region.
          <span v-if="route.query.prompt">
            Based on your request: "{{ route.query.prompt }}"
          </span>
        </p>
      </div>

      <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
        <strong>Error:</strong> {{ error }}
      </div>

      <RoadMapFlowchart :nodes="nodes"/>
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
        <button
            @click="generateRoadmap(route.query.prompt)"
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
        <p class="ml-5" id ="suggested-program" style="color: #FFF3C2;">{{ suggestedProgram }}</p> </li>
        <li>
        <div class="flex items-center space-x-2 mb-2"> <div class="w-3 h-3 rounded-full" style="background-color: #FFD700;"></div>
        <span style="color: #D2C179;">Why this program:</span>
        </div>
        <p class="ml-5" style="color: #FFF3C2;">{{ whyThisProgram }}</p> </li>
      
    </ul>
  </div>
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
