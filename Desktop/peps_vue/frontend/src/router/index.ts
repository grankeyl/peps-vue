import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EarnView from '../views/EarnView.vue'
import UpgradesView from '../views/UpgradesView.vue'
import ShopView from '../views/ShopView.vue'
import ProfileView from '../views/ProfileView.vue'
import TutorialView from '@/views/TutorialView.vue'
import LoadView from '@/views/LoadView.vue'
import DailyView from '@/views/DailyView.vue'
import QrView from '@/views/QrView.vue'
import ChestView from '@/views/ChestView.vue'
import ChestDevView from '@/views/ChestDevView.vue'
import ReferalsView from '@/views/ReferalsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/earn',
      name: 'earn',
      component: EarnView
    },
    {
      path: '/upgrades',
      name: 'upgrades',
      component: UpgradesView
    },
    {
      path: '/shop',
      name: 'shop',
      component: ShopView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/tutorial',
      name: 'tutorial',
      component: TutorialView
    },
    {
      path: '/load',
      name: 'load',
      component: LoadView
    },
    {
      path: '/daily',
      name: 'daily',
      component: DailyView
    },
    {
      path: '/qr',
      name: 'qr',
      component: QrView
    },
    {
      path: '/chest',
      name: 'chest',
      component: ChestView
    },
    {
      path: '/chestDev',
      name: 'chestDev',
      component: ChestDevView
    },
    {
      path: '/referals',
      name: 'referals',
      component: ReferalsView
    }
  ]
})

export default router