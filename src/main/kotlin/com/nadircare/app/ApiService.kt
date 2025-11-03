package com.meddiagnose.app

import okhttp3.MultipartBody
import retrofit2.Response
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

interface ApiService {
    @Multipart
    @POST("upload")
    suspend fun uploadReport(
        @Part file: MultipartBody.Part
    ): Response<AnalysisResponse>
}

