import QtQuick 2.15
import QtQuick.Controls.Basic 2.15
import QtQuick.Layouts 2.15
import "../../themes"
import "../../components"

Button {
    id: datePickerButton

    property bool yearVisible: true

    property alias year: pickerView.value3
    property alias month: pickerView.value1
    property alias monthIndex: pickerView.index1
    property alias day: pickerView.value2

    property int startYear: 1925
    property int endYear: 2125

    readonly property var monthModel: (new Array(12)).fill(0).map((_, i) => i + 1).map(getMonthName)
    readonly property int maxDays: new Date(pickerView.value3 || new Date().getFullYear(), pickerView.index1 + 1, 0).getDate()

    implicitWidth: 250
    padding: 0

    property string date: {
        if (!pickerView.gotData) return ""
        let y = typeof year === "number"? parseInt(year) : new Date().getFullYear()
        let m = parseInt(monthModel.indexOf(month) + 1)
        let d = parseInt(day)
        return y + "-" + m + "-" + d
    }

    function setDate(yyyymmdd) {
        // format
        if (!yyyymmdd || typeof yyyymmdd !== "string"
            || !yyyymmdd.match(/^\d{4}[-\/]\d{1,2}[-\/]\d{1,2}$/))
            return false
        let parts = yyyymmdd.split(/[-\/]/)  // 使用正则分割符号 '-' 或 '/'
        let y = parseInt(parts[0])
        let m = parseInt(parts[1])
        let d = parseInt(parts[2])

        if (m >= 1 && m <= 12 && d >= 1 && d <= 31) {
            pickerView.value3 = y.toString()
            pickerView.value1 = getMonthName(m)
            pickerView.value2 = d.toString()
            pickerView.gotData = true
            return true
        }
        return -1
    }

    // 根据 locale 决定顺序
    property var dateOrder: {
        let fmt = Qt.locale().dateFormat(Locale.ShortFormat)
        let order = []
        if (fmt.indexOf("y") < fmt.indexOf("M") && fmt.indexOf("M") < fmt.indexOf("d"))
            order = ["year", "month", "day"]
        else if (fmt.indexOf("M") < fmt.indexOf("d") && fmt.indexOf("d") < fmt.indexOf("y"))
            order = ["month", "day", "year"]
        else if (fmt.indexOf("d") < fmt.indexOf("M") && fmt.indexOf("M") < fmt.indexOf("y"))
            order = ["day", "month", "year"]

        if (!yearVisible) {
            order = order.filter(item => item !== "year")
        }
        return order
    }

    // locale获取月份名称
    function getMonthName(num) {
        return datePicker.locale.monthName(num - 1)
    }

    onClicked: pickerView.open()

    contentItem: RowLayout {
        anchors.fill: parent
        spacing: 0

        Repeater {
            model: dateOrder

            delegate: Item {
                Layout.fillWidth: true
                Layout.maximumWidth: datePickerButton.implicitWidth / model.length
                implicitHeight: 32

                Text {
                    anchors.centerIn: parent
                    color: pickerView.gotData ? Theme.currentTheme.colors.textColor
                        : Theme.currentTheme.colors.textSecondaryColor

                    text: {
                        const type = modelData
                        if (!pickerView.gotData) {
                            if (type === "year") return qsTr("year")
                            if (type === "month") return qsTr("month")
                            if (type === "day") return qsTr("day")
                        }
                        if (type === "year") return year
                        if (type === "month") return month
                        if (type === "day") return day
                        return ""
                    }
                }
                ToolSeparator {
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    implicitHeight: parent.implicitHeight
                    visible: index !== dateOrder.length - 1
                }
            }
        }
    }

    PickerView {
        id: pickerView
        width: parent.width

        model3: yearVisible
            ? (
                startYear <= endYear
                ? Array.apply(null, {length: endYear - startYear + 1}).map((_, i) => startYear + i)
                : []
            )
            : undefined
        model1: monthModel
        model2: Array.from({ length: maxDays }, (_, i) => i + 1) // 天

        // 初始值
        value3: yearVisible ? (new Date().getFullYear()) : undefined
        value1: getMonthName(new Date().getMonth() + 1)
        value2: new Date().getDate()
        gotData: false

        onValueChanged: gotData = true
    }
}
