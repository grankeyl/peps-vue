import { onMounted } from 'vue'
import { createUser, getUser } from '@/utils/apiRequest'
import { UserStorage } from '@/stores/userStore'
import { TelegramStorage } from '@/stores/telegramStore'
import { RequestStorage } from '@/stores/requestStore'
import { useRouter } from 'vue-router';

import { getLocalization } from '@/utils/apiRequest'
import { LocalizationStorage } from '@/stores/localizationStore'

export async function useUserSetup() {
  const router = useRouter()

  const userStorage = UserStorage()
  const telegramStorage = TelegramStorage()
  const requestStorage = RequestStorage()
  const localizationStorage = LocalizationStorage()

  const userId = telegramStorage.getUserId()
  const firstName = telegramStorage.getUserFirstName()
  const lastName = telegramStorage.getUserLastName()
  const fullName = telegramStorage.getUserFullName()
  const username = telegramStorage.getUserUsername()
  const startParam = telegramStorage.getUserStartParam()
  const photo = telegramStorage.getUserPhoto()

  if (!userId || !firstName || !lastName || !fullName || !username || !photo || !startParam) {
    return
  }

  const response = await createUser(
    userId,
    firstName,
    lastName,
    fullName,
    username,
    photo,
    startParam
  )

  requestStorage.setResponse(response)

  if (response.success) {
    if (startParam !== 'None') {
      location.href = `/tutorial?ref=true`
    } else {
      location.href = `/tutorial?ref=false`
    }
    const userData = await getUser(userId)
    if (userData.success) {
      userStorage.setUser(userData.data.user)
      userStorage.setSettings(userData.data.settings)
      userStorage.setCosts(userData.data.costs)
    }
  } else if (!response.success && response.error === 'exists') {
    const userData = await getUser(userId)
    if (userData.success) {
      userStorage.setUser(userData.data.user)
      userStorage.setSettings(userData.data.settings)
      userStorage.setCosts(userData.data.costs)
    }
  } else {
    // location.reload()
  }

  const localization = await getLocalization()

  if (localization.success) {
    const localizationData = localization.localization
    localizationStorage.setLocalization(localizationData)
  }
}
