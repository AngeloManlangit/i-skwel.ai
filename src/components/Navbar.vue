<template>

  <header class="px-6 py-4 border-b border-yellow-400" style="background-color: #14161a;">
    <div class="max-w-7xl mx-auto flex items-center justify-between" style="background-color: #14161a;">
            <div class=" flex items-center space-x-2">
              <img src="/notext.png" alt="logo" class="w-10 h-10 object-contain">
              <span class="text-yellow-400 text-xl font-bold mt-1">i-skwel.ai</span>
            </div>
            <nav class="flex items-center space-x-8">
              <button @click="$emit('scrollToHome')"
                  class="text-yellow-300 hover:text-yellow-400 transition-colors">
                  Home
              </button>
              <a href="https://www.deped.gov.ph/wp-content/uploads/2019/01/Science-Technology-Engineering-and-Mathematics-STEM-Strand.pdf"
                 class="text-white hover:text-yellow-400 transition-colors"
                 target="_blank"
                 rel="noopener noreferrer">
                 STEM Track</a>
            </nav>
            <button @click="$emit('scrollToRoadmap')"
              class="px-6 py-2 rounded-lg font-semibold text-black bg-gradient-to-r from-yellow-400 to-yellow-300 hover:bg-yellow-300 hover:text-black transition-colors focus:outline-none focus:ring-2 focus:ring-yellow-500">
              Get Started
            </button>
          </div>
        </header>
    
    </template>
    
    <script setup>
  
    defineEmits(['scrollToRoadmap', 'scrollToHome']);
    </script>
    
    <style scoped>
    
    </style>