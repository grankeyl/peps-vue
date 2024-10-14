import { TelegramStorage } from '@/stores/telegramStore'
import { LocalizationStorage } from '@/stores/localizationStore'
import { onMounted } from 'vue'
import { DEVELOPER_MODE, TELEGRAM_BOT, TEST_USER_ID } from '@/config'
import { useUserSetup } from './useUserSetup'
import { getLocalization } from '@/utils/apiRequest'

export async function useTelegramSetup() {
  onMounted(async () => {
    const telegramStorage = TelegramStorage()
    const localizationStorage = LocalizationStorage()

    if (window.Telegram) {
      const tg_safe = window.Telegram.WebApp

      tg_safe.ready()
      tg_safe.expand()
      tg_safe.disableVerticalSwipes()

      tg_safe.SettingsButton.show()

      tg_safe.isClosingConfirmationEnabled = true
      tg_safe.headerColor = '#13192F'
      tg_safe.backgroundColor = '#13192F'

      const tg_unsafe = tg_safe.initDataUnsafe || {}

      let tg_user_id,
        tg_first_name,
        tg_last_name,
        tg_full_name,
        tg_username,
        tg_photo,
        tg_language,
        tg_start_param,
        tg_premium

      if ('user' in tg_unsafe) {
        tg_user_id = tg_unsafe.user?.id || 'None'
        tg_first_name = tg_unsafe.user?.first_name || ' '
        tg_last_name = tg_unsafe.user?.last_name || ' '
        tg_full_name = `${tg_first_name} ${tg_last_name}`.trim()
        tg_username = tg_unsafe.user?.username || 'None'
        tg_photo = tg_unsafe.user?.photo || 'None'
        tg_language = tg_unsafe.user?.language_code || 'en'

        // это параметр после startapp=
        tg_start_param = tg_unsafe?.start_param || 'None'
        // tg_premium = tg_unsafe.user?.is_premium || true
        tg_premium = true
      } else {
        tg_user_id = TEST_USER_ID
        tg_first_name = 'first_name'
        tg_last_name = 'last_name'
        tg_full_name = `${tg_first_name} ${tg_last_name}`
        tg_username = 'username'
        tg_photo = 'None'
        tg_language = 'en'

        // это параметр после startapp=
        tg_start_param = 'None'

        tg_premium = true
      }

      telegramStorage.setUserId(tg_user_id)
      telegramStorage.setUserFirstName(tg_first_name)
      telegramStorage.setUserLastName(tg_last_name)
      telegramStorage.setUserFullName(tg_full_name)
      telegramStorage.setUserUsername(tg_username)
      telegramStorage.setUserPhoto(tg_photo)
      telegramStorage.setUserLanguage(tg_language)
      telegramStorage.setUserStartParam(tg_start_param)
      telegramStorage.setUserIsPremium(tg_premium)
      telegramStorage.setUserStartParam(tg_start_param)

      await useUserSetup()

    } else {
      console.log('Telegram is not defined.')
    }
  })
}

export function vibrateTelegram(type, options = {}) {
  const tg_safe = window.Telegram.WebApp

  if (tg_safe.HapticFeedback) {
    try {
      switch (type) {
        case 'impact':
          tg_safe.HapticFeedback.impactOccurred(options.impact_style || 'light')
          break
        case 'notification':
          tg_safe.HapticFeedback.notificationOccurred(options.notification_type || 'success')
          break
        case 'selection_change':
          tg_safe.HapticFeedback.selectionChanged()
          break
      }
    } catch {
      return
    }
  }
}

export function settingsTelegram(toggleSettings, type) {
  if (window.Telegram) {
    const tg_safe = window.Telegram.WebApp

    let eventHandled = false

    function callback() {
      if (!eventHandled) {
        console.log('Callback function called')
        eventHandled = true
      }
    }

    if (type === 'profile') {
      toggleSettings()
      callback()
    } else {
      tg_safe.onEvent('settingsButtonClicked', () => {
        toggleSettings()
        callback()
      })
    }
  } else {
    console.log('Telegram is not defined.')
  }
}

export function shareStory(referal_key: string, language: string) {
  const tg_safe = window.Telegram.WebApp

  if (window.Telegram) {
    const storiesList = []

    for (let i = 1; i <= 12; i++) {
      if (language == 'ru') {
        storiesList.push(`/src/assets/stories/ru/${i}.png`)
      } else {
        storiesList.push(`/src/assets/stories/en/${i}.png`)
      }
    }

    const randomIndex = Math.floor(Math.random() * storiesList.length)
    const mediaUrl = storiesList[randomIndex]

    const storyParams = {
      text:
        language == 'ru'
          ? `🐸 Какой ты Пепе?\n👉 Узнать — https://t.me/${TELEGRAM_BOT}/app?startapp=${referal_key}`
          : `🐸 What Pepe are You?\n👉 Check out — https://t.me/${TELEGRAM_BOT}/app?startapp=${referal_key}`,
      widget_link: {
        url: `https://t.me/${TELEGRAM_BOT}/app?startapp=${referal_key}`,
        name: language == 'ru' ? 'УЗНАЙ КАКОЙ ТЫ ПЕПЕ' : 'WHAT PEPE ARE YOU?'
      }
    }

    try {
      tg_safe.shareToStory(mediaUrl, storyParams)
    } catch (e) {
      console.log(e)
    }
  }
}

export function telegramLink(link: string) {
  const tg_safe = window.Telegram.WebApp

  if (window.Telegram) {
    tg_safe.openTelegramLink(link)
  }
}

export function telegramDefaultLink(link: string) {
  const tg_safe = window.Telegram.WebApp

  if (window.Telegram) {
    tg_safe.openLink(link)
  }
}
