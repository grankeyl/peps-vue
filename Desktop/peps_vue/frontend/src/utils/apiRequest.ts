import axios from 'axios'
import { API_URL } from '@/config'

async function apiRequest(path: string, params: Object) {
  const url = `${API_URL}/${path}`
  const response = await axios.get(url, { params })
  return response.data
}

export const createUser = async (
  userId: string,
  firstName: string,
  lastName: string,
  fullName: string,
  username: string,
  photoId: string
) => {
  const response = await apiRequest('user/create', {
    user_id: userId,
    first_name: firstName,
    last_name: lastName,
    full_name: fullName,
    username: username,
    photo_id: photoId
  })

  return response
}

export const getUser = async (userId: string) => {
  const response = await apiRequest('user/get', {
    user_id: userId
  })

  return response
}

export const updateGame = async (userId: string, views: any, earn: any, ton: any, stamina: any) => {
  const response = await apiRequest('user/updateGame', {
    user_id: userId,
    views: views,
    earn: earn,
    ton: ton,
    stamina: stamina
  })

  return response
}

export const getFullStamina = async (userId: string) => {
  const response = await apiRequest('user/get/full_stamina', {
    user_id: userId
  })
  return response
}

export const updateFullStamina = async (userId: string) => {
  const response = await apiRequest('user/update/full_stamina', {
    user_id: userId
  })
  return response
}

export const buy = async (userId: string, type: string, amount: any) => {
  const response = await apiRequest('user/update/buy', {
    user_id: userId,
    type: type,
    amount: amount
  })
  return response
}

export const updateChances = async (
  userId: string,
  views_chance: string,
  money_chance: string,
  new_cost: string,
  type: string
) => {
  const response = await apiRequest('user/update/post_chances', {
    user_id: userId,
    view_chance: views_chance,
    money_chance: money_chance,
    new_cost: new_cost,
    type: type
  })
  return response
}

export const setSettings = async (userId: string, language: string, tap_animation: boolean) => {
  const response = await apiRequest('user/update/settings', {
    user_id: userId,
    language: language,
    tap_animation: tap_animation
  })
  return response
}

export const getShopItems = async () => {
  const response = await apiRequest('shop/items', {})
  return response
}

export const getSkins = async (userId: string) => {
  const response = await apiRequest('user/getSkins', {
    user_id: userId
  })
  return response
}

export const getPutonSkins = async (userId: string) => {
  const response = await apiRequest('user/getPutonSkins', {
    user_id: userId
  })
  return response
}

export const upgradeSkin = async (userId: string, skinId: string, upgrade: object) => {
  const response = await apiRequest('user/upgradeSkin', {
    user_id: userId,
    skin_id: skinId,
    upgrade: upgrade
  })
  return response
}

export const buySkin = async (userId: string, skinId: string) => {
  const response = await apiRequest('user/buySkin', {
    user_id: userId,
    skin_id: skinId
  })
  return response
}
