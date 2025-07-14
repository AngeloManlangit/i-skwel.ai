<template>
    <div class="min-h-screen" style="background-color: #14161a;">
  
      <Navbar @scrollToRoadmap="initiateRoadmapGenerationFromGetStarted" @scrollToHome="handleNavigateToHome" />
  
      <div :class="{ 'blur-sm': showRoadmapLoading, 'pointer-events-none': showRoadmapLoading }"
           class="transition-all duration-300 ease-out pt-30">
        <section id="home-section" class="px-6 py-16">
          <div class="max-w-4xl mx-auto text-center">
            <div class="px-4 py-2 inline-block rounded-full mb-12 border border-yellow-400" style="background-color: #ffd7001a;">
              <span style="color: #d2c179">🚀 Built for Ambitious STEM Students in Cebu</span>
            </div>
  
            <h1 class="font-bold text-center text-5xl mb-4 leading-tight">
              <span class="drop-shadow-[0_0_30px_#FFF3C2] - text-[#fff3c2]">Your </span>
              <span class="drop-shadow-[0_0_5px_#FFD700] - text-[#FFD700]">AI-Powered </span>
              <span class="drop-shadow-[0_0_30px_#FFF3C2] - text-[#fff3c2]">Learning </span><br>
              <span class="drop-shadow-[0_0_30px_#FFD700] - text-[#FFD700]">Roadmap to Success</span>
            </h1>
  
            <p class="font-bold text-xl mt-4 mb-6" style="color: #d2c179;">
              Gusto ko mahimong <span class ="italic">{{ animatedText }}</span>
            </p>
  
            <p class="text-lg mb-12 max-w-3xl mx-auto" style="color: #d2c179">
              Get personalized learning and career development paths tailored for STEM students in Cebu City.
              Create your own actionable pathways with resources and opportunities for a brighter future.
            </p>
  
            <div class="flex flex-wrap gap-4 justify-center mb-16">
              <div class="flex items-center space-x-2">
                <div class="w-2 h-2 rounded-full" style="background-color:yellow;"></div>
                <span style="color:#d2c179">Ignited Curiosity</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-2 h-2 rounded-full" style="background-color:yellow;"></div>
                <span style="color:#d2c179">Personalized Learnings</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-2 h-2 rounded-full" style="background-color:yellow;"></div>
                <span style="color:#d2c179">AI-Driven Insights</span>
              </div>
            </div>
  
            <div
              id="roadmap-form-section" ref="roadmapBox"
              class="max-w-2xl mx-auto p-6 rounded-2xl border-2 transition-shadow duration-500"
              :class="{ 'ring-4 ring-yellow-400': isHighlighted }"
              style="border-color: #FFD700; background-color: #ffd7000d;">
              <h2 class="text-2xl font-bold mb-6 bg-gradient-to-r from-yellow-500 to-yellow-200 bg-clip-text text-transparent">Create Your Learning Roadmap</h2>
  
              <div class="mb-4">
                <div class="flex items-center justify-between space-x-2 mb-2">
                  <div class="flex items-center space-x-2">
                    <div class="w-3 h-3 rounded-full" style="background-color: #FFD700;"></div>
                    <span style="color: #D2C179;">Provide a thorough overview of who you are.</span>
                  </div>
                  <span class="text-sm" style="color: #D2C179;">{{ overviewText?.length || 0 }}/{{ maxChars }}</span>
                </div>
                <textarea
                  v-model="overviewText"
                  class="w-full p-4 rounded-lg border-0 resize-none h-24"
                  style="background-color: #14181C; color: #FFF3C2;"
                  placeholder="What are your interests? What are your skills? What are your weaknesses?"
                  maxlength="1000"
                ></textarea>
              </div>
  
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div>
                  <label class="block mb-2" style="color: #D2C179;">Your Location (Optional)</label>
                  <textarea
                    v-model="userInput.location"
                    class="w-full p-4 rounded-lg border-0 resize-none h-24"
                    style="background-color: #14181C; color: #FFF3C2;"
                    placeholder="Location may enhance university options insights."
                  ></textarea>
                </div>
                <div>
                  <label class="block mb-2" style="color: #D2C179;">Starting Point</label>
                  <select v-model="userInput.startingPoint" class="w-full p-3 rounded-lg border-0" style="background-color: #14181C; color: #FFF3C2;">
                    <option value="College">College</option>
                    <option value="Senior High School">Senior High School</option>
                    </select>
                </div>
              </div>
  
              <button
                @click="initiateRoadmapGeneration"
                class="w-full py-4 rounded-lg font-bold text-black text-lg transition-colors hover:opacity-90"
                style="background-color: #FFD700;">
                Generate Roadmap 🚀
              </button>
            </div>
          </div>
        </section>
  
      </div>
  
      <transition name="fade">
        <div v-if="showRoadmapLoading" class="fixed inset-0 flex items-center justify-center z-50 backdrop-blur-sm" style="background-color: rgba(0, 0, 0, 0.7);">
          <div class="text-center">
            <img src="/loading.gif" alt="notext" class="w-32 h-32 object-contain mx-auto mb-4 animate-pulse">
            <p class="text-yellow-400 text-xl font-semibold">Generating your personalized roadmap...</p>
          </div>
        </div>
      </transition>
  
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch, nextTick } from 'vue';
  import { useRoute, useRouter } from 'vue-router'; 
  
  import Navbar from './Navbar.vue';
  
  const route = useRoute();
  const router = useRouter();
  
  const showRoadmapLoading = ref(false);
  
  
  const userInput = ref({
    interests: '',
    location: '',
    startingPoint: 'College' 
  });
  
  const overviewText = ref('');
  const maxChars = 1000;
  
  const words = [
    'doctor.',
    'engineer.',
    'chemist.',
    'teacher.',
    'computer scientist.'
  ];
  const wordIndex = ref(0);
  const animatedText = ref('');
  const isDeleting = ref(false);
  const typingSpeed = 100;
  const deletingSpeed = 50;
  const delayAfterWord = 1500;
  const delayAfterDelete = 500;
  
  const typeEffect = () => {
    const currentWord = words[wordIndex.value % words.length];
    if (isDeleting.value) {
      animatedText.value = currentWord.substring(0, animatedText.value.length - 1);
    } else {
      animatedText.value = currentWord.substring(0, animatedText.value.length + 1);
    }
    let currentSpeed = isDeleting.value ? deletingSpeed : typingSpeed;
    if (!isDeleting.value && animatedText.value === currentWord) {
      currentSpeed = delayAfterWord;
      isDeleting.value = true;
    }
    else if (isDeleting.value && animatedText.value === '') {
      isDeleting.value = false;
      wordIndex.value++;
      currentSpeed = delayAfterDelete;
    }
    setTimeout(typeEffect, currentSpeed);
  };
  
  const roadmapBox = ref(null);
  const isHighlighted = ref(false);
  
  
  async function generateRoadmapData(data) {
    console.log("Simulating API call to generate roadmap with data:", data);
  
  
  
  }
  
  
  const initiateRoadmapGeneration = () => {
    showRoadmapLoading.value = true;
  
    setTimeout(async () => {
      try {
        // Collect all necessary user input
        const dataToGenerate = {
          interests: overviewText.value,
          location: userInput.value.location,
          startingPoint: userInput.value.startingPoint
        };
  
        // Call the local API generation function
        const generatedRoadmapData = await generateRoadmapData(dataToGenerate);
  
        showRoadmapLoading.value = false;
  
        
        router.push({
          name: 'Roadmap',
          query: {
            prompt: overviewText.value, 
            location: userInput.value.location,
            startingPoint: userInput.value.startingPoint,
         
          }
        });
      } catch (err) {
        console.error("Error initiating roadmap generation:", err);
        // You might want to display an error message to the user here
        showRoadmapLoading.value = false;
        // Optionally, navigate to an error page or show a modal
      }
    }, 2000); 
  };
  
  
  const initiateRoadmapGenerationFromGetStarted = () => {
    
    if (roadmapBox.value) {
      roadmapBox.value.scrollIntoView({ behavior: 'smooth' });
      isHighlighted.value = true;
      setTimeout(() => {
        isHighlighted.value = false;
      }, 1500); 
    }
  };
  
  // Function to handle navigation to the Home section
  const handleNavigateToHome = () => {
    const homeSection = document.getElementById('home-section');
    if (homeSection) {
      homeSection.scrollIntoView({ behavior: 'smooth' });
    }
  };
  
  watch(
    () => route.hash,
    (newHash) => {
      if (newHash) {
        nextTick(() => {
          const targetElement = document.querySelector(newHash);
          if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth' });
          }
        });
      }
    }
  );
  
  onMounted(() => {
    typeEffect();
  });
  </script>
  
  <style scoped>
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