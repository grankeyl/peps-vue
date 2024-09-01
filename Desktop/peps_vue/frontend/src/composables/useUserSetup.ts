import { onMounted } from 'vue'
import { createUser, getUser } from '@/utils/apiRequest'
import { UserStorage } from '@/stores/userStore'
import { TelegramStorage } from '@/stores/telegramStore'
import { RequestStorage } from '@/stores/requestStore'

export async function useUserSetup() {
  const userStorage = UserStorage()
  const telegramStorage = TelegramStorage()
  const requestStorage = RequestStorage()

  const userId = telegramStorage.getUserId()
  const firstName = telegramStorage.getUserFirstName()
  const lastName = telegramStorage.getUserLastName()
  const fullName = telegramStorage.getUserFullName()
  const username = telegramStorage.getUserUsername()
  const photo = telegramStorage.getUserPhoto()

  if (!userId || !firstName || !lastName || !fullName || !username || !photo) {
    return
  }

  const response = await createUser(userId, firstName, lastName, fullName, username, photo)
  requestStorage.setResponse(response)
  if (response.success) {
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
    // window.location.reload()
  }
}
