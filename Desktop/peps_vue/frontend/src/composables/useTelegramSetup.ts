import { TelegramStorage } from '@/stores/telegramStore'
import { onMounted } from 'vue'
import { DEVELOPER_MODE } from '@/config'
import { useUserSetup } from './useUserSetup'

export async function useTelegramSetup() {
  onMounted(async () => {
    const telegramStorage = TelegramStorage()
    if (window.Telegram) {
      const tg_safe = window.Telegram.WebApp

      const tg_unsafe = tg_safe.initDataUnsafe || {}

      let tg_user_id,
        tg_first_name,
        tg_last_name,
        tg_full_name,
        tg_username,
        tg_photo,
        tg_language,
        tg_start_param

      if (!DEVELOPER_MODE) {
        tg_user_id = tg_unsafe.user?.id || 'None'
        tg_first_name = tg_unsafe.user?.first_name || 'None'
        tg_last_name = tg_unsafe.user?.last_name || 'None'
        tg_full_name = `${tg_first_name} ${tg_last_name}`.trim()
        tg_username = tg_unsafe.user?.username || 'None'
        tg_photo = tg_unsafe.user?.photo || 'None'
        tg_language = tg_unsafe.user?.language_code || 'en'
        tg_start_param = tg_unsafe.user?.start_param || 'None'
      } else {
        tg_user_id = 100000003
        tg_first_name = 'first_name'
        tg_last_name = 'last_name'
        tg_full_name = `${tg_first_name} ${tg_last_name}`
        tg_username = 'username'
        tg_photo = 'None'
        tg_language = 'en'
        tg_start_param = 'None'
      }

      tg_safe.ready()
      tg_safe.expand()
      tg_safe.disableVerticalSwipes()

      tg_safe.isClosingConfirmationEnabled = true
      tg_safe.headerColor = '#13192F'
      tg_safe.backgroundColor = '#13192F'

      telegramStorage.setUserId(tg_user_id)
      telegramStorage.setUserFirstName(tg_first_name)
      telegramStorage.setUserLastName(tg_last_name)
      telegramStorage.setUserFullName(tg_full_name)
      telegramStorage.setUserUsername(tg_username)
      telegramStorage.setUserPhoto(tg_photo)
      telegramStorage.setUserLanguage(tg_language)
      telegramStorage.setUserStartParam(tg_start_param)

      await useUserSetup()
    } else {
      console.error('Telegram is not defined.')
    }
  })
}
