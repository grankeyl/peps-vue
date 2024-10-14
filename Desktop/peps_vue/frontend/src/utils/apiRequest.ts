import axios from 'axios'
import { API_URL, SECRET_KEY } from '@/config'

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
  photoId: string,
  startParam: string
) => {
  const response = await apiRequest('user/create', {
    key: SECRET_KEY,
    user_id: userId,
    first_name: firstName,
    last_name: lastName,
    full_name: fullName,
    username: username,
    photo_id: photoId,
    invited_by: startParam
  })

  return response
}

export const getUser = async (userId: string) => {
  const response = await apiRequest('user/get', {
    key: SECRET_KEY,
    user_id: userId
  })

  return response
}

export const updateGame = async (
  userId: string,
  views: any,
  earn: any,
  ton: any,
  stamina: any,
  experience: any
) => {
  const response = await apiRequest('user/updateGame', {
    key: SECRET_KEY,
    user_id: userId,
    views: views,
    earn: earn,
    ton: ton,
    stamina: stamina,
    experience: experience
  })

  return response
}

export const getFullStamina = async (userId: string) => {
  const response = await apiRequest('user/get/full_stamina', {
    key: SECRET_KEY,
    user_id: userId
  })
  return response
}

export const updateFullStamina = async (userId: string) => {
  const response = await apiRequest('user/update/full_stamina', {
    key: SECRET_KEY,
    user_id: userId
  })
  return response
}

export const buy = async (userId: string, type: string, amount: any) => {
  const response = await apiRequest('user/update/buy', {
    key: SECRET_KEY,
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
    key: SECRET_KEY,
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
    key: SECRET_KEY,
    user_id: userId,
    language: language,
    tap_animation: tap_animation
  })
  return response
}

export const getShopItems = async (userId: string) => {
  const response = await apiRequest('shop/items', {
    key: SECRET_KEY,
    userId: userId
  })
  return response
}

export const getSkins = async (userId: string) => {
  const response = await apiRequest('user/getSkins', {
    key: SECRET_KEY,
    user_id: userId
  })
  return response
}

export const getPutonSkins = async (userId: string) => {
  const response = await apiRequest('user/getPutonSkins', {
    key: SECRET_KEY,
    user_id: userId
  })
  return response
}

export const upgradeSkin = async (
  userId: string,
  skinId: string,
  upgrade: object,
  baffs: object
) => {
  const response = await apiRequest('user/upgradeSkin', {
    key: SECRET_KEY,
    user_id: userId,
    skin_id: skinId,
    upgrade: upgrade,
    baffs: baffs
  })
  return response
}

export const buySkin = async (userId: string, skinId: string) => {
  const response = await apiRequest('user/buySkin', {
    key: SECRET_KEY,
    user_id: userId,
    skin_id: skinId
  })
  return response
}

export const changeSkin = async (userId: string, skinId: string) => {
  const response = await apiRequest('user/skinChange', {
    key: SECRET_KEY,
    user_id: userId,
    skin_id: skinId
  })

  return response
}

export const unPutSkin = async (userId: string, skinId: string) => {
  const response = await apiRequest('user/unPutSkin', {
    key: SECRET_KEY,
    user_id: userId,
    skin_id: skinId
  })

  return response
}

export const getUserTasks = async (userId: string) => {
  const response = await apiRequest('tasks/get', {
    key: SECRET_KEY,
    user_id: userId
  })

  return response
}

export const getTask = async (taskId: string, userId: string) => {
  const response = await apiRequest('tasks/getTask', {
    key: SECRET_KEY,
    task_id: taskId,
    user_id: userId
  })

  return response
}

export const taskNextStep = async (taskId: string, userId: string) => {
  const response = await apiRequest('tasks/task/nextStep', {
    key: SECRET_KEY,
    task_id: taskId,
    user_id: userId
  })

  return response
}

export const endTask = async (taskId: string, userId: string, views: any, earn: any, ton: any) => {
  const response = await apiRequest('tasks/task/endTask', {
    key: SECRET_KEY,
    task_id: taskId,
    user_id: userId,
    views: views,
    earn: earn,
    ton: ton
  })

  return response
}

export const checkSubscribe = async (user_id: any, channel_id: any) => {
  const response = await apiRequest('misc/checkSubscribe', {
    key: SECRET_KEY,
    user_id: user_id,
    channel_id: channel_id
  })

  return response
}

export const getDailyAll = async () => {
  const response = await apiRequest('daily/get_all', {
    key: SECRET_KEY
  })

  return response
}

export const getDailyGift = async (userId: any) => {
  const response = await apiRequest('daily/get_gift', {
    key: SECRET_KEY,
    user_id: userId
  })

  return response  
}

export const updateBalance = async (
  userId: any,
  typeAmount: any,
  amount: any
) => {
  const response = await apiRequest('user/update/balance', {
    key: SECRET_KEY,
    user_id: userId,
    type: typeAmount,
    amount: amount
  })

  return response
}

export const getChests = async () => {
  const response = await apiRequest('chests/chests_get', {
    key: SECRET_KEY
  })
  return response
}

export const getReferals = async (userId: any) => {
  const response = await apiRequest('user/get_referals', {
    key: SECRET_KEY,
    user_id: userId
  })

  return response
}

export const getAvatar = async (userId: any) => {
  const response = await apiRequest('misc/getAvatar', {
    key: SECRET_KEY,
    user_id: userId
  })
  return response
}

export const addExperience = async (userId: any, experience: any) => {
  const response = await apiRequest('user/addExperience', {
    key: SECRET_KEY,
    user_id: userId,
    experience: experience
  })
  return response
}

export const afkStamina = async (userId: any) => {
  const response = await apiRequest('user/afkStamina', {
    key: SECRET_KEY,
    user_id: userId
  })
  return response
}

export const shopBandles = async (userId: any, typeBandle: string, amountBandle: any) => {
  const response = await apiRequest('stars/shopBandles', {
    key: SECRET_KEY,
    user_id: userId,
    type_bandle: typeBandle,
    amount_bandle: amountBandle
  })
  return response
}

export const createStarsLink = async (
  userId: any,
  invoiceTitle: string,
  invoiceDescription: string,
  invoiceAmount: number,
  invoicePhoto: string,
  invoiceParams: object
) => {
  const response = await apiRequest('misc/createStarsLink', {
    key: SECRET_KEY,
    user_id: userId,
    invoice_title: invoiceTitle,
    invoice_description: invoiceDescription,
    invoice_amount: invoiceAmount,
    invoice_photo: invoicePhoto,
    invoice_params: invoiceParams
  })
  return response
}

export const getInvoice = async (
  invoice_id: string
) => {
  const response = await apiRequest('misc/getInvoice', {
    key: SECRET_KEY,
    invoice_id: invoice_id
  })
  return response
}

export const existsInvoice = async (
  invoice_id: string
) => {
  const response = await apiRequest('misc/existsInvoice', {
    key: SECRET_KEY,
    invoice_id: invoice_id
  })
  return response
}

export const updateSpecials = async (
  userId: string,
  specialId: string
) => {
  const response = await apiRequest('user/updateSpecials', {
    key: SECRET_KEY,
    user_id: userId,
    special_id: specialId
  })
  return response
}

export const sendLogAdmin = async (
  type: string,
  params: object
) => {
  const response = await apiRequest('misc/sendLogAdmin', {
    key: SECRET_KEY,
    type: type,
    params: JSON.stringify(params)
  })
  return response
}

export const getGiftsStars = async (
  userId: any
) => {
  const response = await apiRequest('daily/get_gifts_stars', {
    key: SECRET_KEY,
    user_id: userId
  })
  return response
}

export const getLocalization = async () => {
  const response = await apiRequest('misc/localization', {
    key: SECRET_KEY
  })
  return response
}

export const updateReferals = async (userId: any, referalNeed: number, referalKey: string) => {
  const response = await apiRequest('user/update/friends', {
    key: SECRET_KEY,
    user_id: userId,
    referal_need: referalNeed,
    referal_key: referalKey
  })
  return response
}