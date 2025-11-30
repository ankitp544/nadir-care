package com.nadircare.app

import com.google.gson.annotations.SerializedName

data class AnalysisResponse(
    @SerializedName("recommendation")
    val recommendation: RecommendationType,
    
    @SerializedName("confidence")
    val confidence: Double?,
    
    @SerializedName("reasoning")
    val reasoning: String?,
    
    @SerializedName("suggested_actions")
    val suggested_actions: List<String>?
)

enum class RecommendationType {
    @SerializedName("ADMISSION")
    ADMISSION,
    
    @SerializedName("DOCTOR_VISIT")
    DOCTOR_VISIT,
    
    @SerializedName("HOME_MEDICATION")
    HOME_MEDICATION
}

data class ErrorResponse(
    @SerializedName("detail")
    val detail: String?
)

