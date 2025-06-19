<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8">
        <v-card flat rounded="lg">
          <v-img
            height="200px"
            src="https://images.unsplash.com/photo-1593327914834-3105f24255a6?q=80&w=2000&auto=format&fit=crop"
            class="rounded-t-lg"
          ></v-img>
          <div class="px-6 pb-2">
            <div class="d-flex align-end">
              <v-avatar size="128" class="profile-avatar elevation-4">
                <v-img src="https://i.pravatar.cc/128?u=assaf"></v-img>
              </v-avatar>
              <v-spacer></v-spacer>
              <v-btn variant="outlined" color="grey-darken-1" class="mb-4">
                <v-icon left>mdi-pencil</v-icon>
                Edit Profile
              </v-btn>
            </div>
            <div class="mt-n10 ml-1">
              <h1 class="text-h4 font-weight-bold">Assaf Rappaport</h1>
              <p class="text-subtitle-1">VP of Customer Operations</p>
              <p class="text-body-2 text-grey">San Francisco, CA USA</p>
            </div>
          </div>
          <v-tabs v-model="tab" bg-color="transparent" color="black">
            <v-tab value="overview">Overview</v-tab>
            <v-tab value="groups">Groups</v-tab>
          </v-tabs>
        </v-card>
        <v-window v-model="tab" class="mt-6">
          <v-window-item value="overview">
            <v-card class="pa-4" rounded="lg">
              <v-card-title>
                <v-spacer></v-spacer>
                <v-icon color="grey">mdi-pencil-outline</v-icon>
              </v-card-title>
              <v-card-text class="text-body-1">
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
              </v-card-text>
            </v-card>
          </v-window-item>
        </v-window>
      </v-col>
      <v-col cols="12" md="4">
        <v-card class="pa-2" rounded="lg">
          <v-list class="py-0">
            <v-list-item v-for="person in managerTeam" :key="person.name" :prepend-avatar="person.avatar" :title="person.name" :subtitle="person.title"></v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
const tab = ref('overview');
const managerTeam = ref([
  { name: 'Roy Reznik', title: 'Chief Executive Officer', avatar: 'https://i.pravatar.cc/40?u=roy' },
  { name: 'James Bolosh', title: 'Chief Operating officer', avatar: 'https://i.pravatar.cc/40?u=james' },
  { name: 'Assaf Rappaport', title: 'VP of Customer Operations', avatar: 'https://i.pravatar.cc/40?u=assaf' },
]);
</script>

<style scoped>
.profile-avatar {
  margin-top: -64px;
  border: 4px solid white;
}
</style>